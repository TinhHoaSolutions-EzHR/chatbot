import Cookies from "js-cookie";
import { AuthTypeMetadata, getAuthTypeMetadataSS, getCurrentUserSS } from "@/lib/userSS";
import { redirect } from "next/navigation";
import { HealthCheckBanner } from "@/components/health/healthcheck";
import { fetchSS } from "@/lib/utilsSS";
import { CCPairBasicInfo, DocumentSet, Tag, User } from "@/lib/types";
import { SearchType } from "@/lib/search/interfaces";
import { Persona } from "../admin/assistants/interfaces";
import { unstable_noStore as noStore } from "next/cache";
import { InstantSSRAutoRefresh } from "@/components/SSRAutoRefresh";
import { personaComparator } from "../admin/assistants/lib";
import { FullEmbeddingModelResponse } from "@/components/embedding/interfaces";
import { ChatPopup } from "../chat/ChatPopup";
import { FetchAssistantsResponse, fetchAssistantsSS } from "@/lib/assistants/fetchAssistantsSS";
import { ChatSession } from "../chat/interfaces";
import { SIDEBAR_TOGGLED_COOKIE_NAME } from "@/components/resizable/constants";
import { AGENTIC_SEARCH_TYPE_COOKIE_NAME, NEXT_PUBLIC_DEFAULT_SIDEBAR_OPEN, DISABLE_LLM_DOC_RELEVANCE } from "@/lib/constants";
import WrappedSearch from "./WrappedSearch";
import { SearchProvider } from "@/components/context/SearchContext";
import { fetchLLMProvidersSS } from "@/lib/llm/fetchLLMs";
import { LLMProviderDescriptor } from "../admin/configuration/llm/interfaces";
import { hasCompletedWelcomeFlowSS, WelcomeModal } from "@/components/initialSetup/welcome/WelcomeModalWrapper";

export default async function Home(props: { searchParams: Promise<{ [key: string]: string | string[] | undefined }> }) {
  const searchParams = await props.searchParams;
  noStore();

  const tasks = [
    getAuthTypeMetadataSS(),
    getCurrentUserSS(),
    fetchSS("/manage/indexing-status"),
    fetchSS("/manage/document-set"),
    fetchAssistantsSS(),
    fetchSS("/query/valid-tags"),
    fetchSS("/query/user-searches"),
    fetchLLMProvidersSS(),
  ];

  let results: (
    | User
    | Response
    | AuthTypeMetadata
    | FullEmbeddingModelResponse
    | FetchAssistantsResponse
    | LLMProviderDescriptor[]
    | null
    )[] = [null, null, null, null, null, null, null, null];
  try {
    results = await Promise.all(tasks);
  } catch (e) {
    console.log(`Some fetch failed for the main search page - ${e}`);
  }
  const authTypeMetadata = results[0] as AuthTypeMetadata | null;
  const user = results[1] as User | null;
  const ccPairsResponse = results[2] as Response | null;
  const documentSetsResponse = results[3] as Response | null;
  const [initialAssistantsList, assistantsFetchError] = results[4] as FetchAssistantsResponse;
  const tagsResponse = results[5] as Response | null;
  const queryResponse = results[6] as Response | null;
  const llmProviders = (results[7] || []) as LLMProviderDescriptor[];

  const authDisabled = authTypeMetadata?.authType === "disabled";

  if (!authDisabled && !user) {
    const fullUrl = Cookies.get("x-url") || "/search";
    const searchParamsString = new URLSearchParams(searchParams as unknown as Record<string, string>).toString();
    const redirectUrl = searchParamsString ? `${fullUrl}?${searchParamsString}` : fullUrl;
    return redirect(`/auth/login?next=${encodeURIComponent(redirectUrl)}`);
  }

  if (user && !user.is_verified && authTypeMetadata?.requiresVerification) {
    return redirect("/auth/waiting-on-verification");
  }

  let ccPairs: CCPairBasicInfo[] = [];
  if (ccPairsResponse?.ok) {
    ccPairs = await ccPairsResponse.json();
  } else {
    console.log(`Failed to fetch connectors - ${ccPairsResponse?.status}`);
  }

  let documentSets: DocumentSet[] = [];
  if (documentSetsResponse?.ok) {
    documentSets = await documentSetsResponse.json();
  } else {
    console.log(`Failed to fetch document sets - ${documentSetsResponse?.status}`);
  }

  let querySessions: ChatSession[] = [];
  if (queryResponse?.ok) {
    querySessions = (await queryResponse.json()).sessions;
  } else {
    console.log(`Failed to fetch chat sessions - ${queryResponse?.text()}`);
  }

  let assistants: Persona[] = initialAssistantsList;
  if (assistantsFetchError) {
    console.log(`Failed to fetch assistants - ${assistantsFetchError}`);
  } else {
    assistants = assistants.filter((assistant) => assistant.is_visible && assistant.num_chunks !== 0);
    assistants.sort(personaComparator);
  }

  let tags: Tag[] = [];
  if (tagsResponse?.ok) {
    tags = (await tagsResponse.json()).tags;
  } else {
    console.log(`Failed to fetch tags - ${tagsResponse?.status}`);
  }

  const storedSearchType = Cookies.get("searchType") as string | undefined;
  const searchTypeDefault: SearchType = storedSearchType && SearchType.hasOwnProperty(storedSearchType)
    ? (storedSearchType as SearchType)
    : SearchType.SEMANTIC;

  const hasAnyConnectors = ccPairs.length > 0;

  const shouldShowWelcomeModal = !llmProviders.length &&
    !hasCompletedWelcomeFlowSS(Cookies.get()) &&
    !hasAnyConnectors &&
    (!user || user.role === "admin");

  const shouldDisplayNoSourcesModal = (!user || user.role === "admin") &&
    ccPairs.length === 0 &&
    !shouldShowWelcomeModal;

  const toggleSidebar = Cookies.get(SIDEBAR_TOGGLED_COOKIE_NAME) === "true" || NEXT_PUBLIC_DEFAULT_SIDEBAR_OPEN;
  const agenticSearchEnabled = Cookies.get(AGENTIC_SEARCH_TYPE_COOKIE_NAME) === "true";

  return (
    <>
      <HealthCheckBanner />
      <InstantSSRAutoRefresh />
      {shouldShowWelcomeModal && (
        <WelcomeModal user={user} requestCookies={Cookies.get()} />
      )}
      <ChatPopup />
      <SearchProvider value={{
        querySessions,
        ccPairs,
        documentSets,
        assistants,
        tags,
        agenticSearchEnabled,
        disabledAgentic: DISABLE_LLM_DOC_RELEVANCE,
        initiallyToggled: toggleSidebar,
        shouldShowWelcomeModal,
        shouldDisplayNoSources: shouldDisplayNoSourcesModal,
      }}
      >
        <WrappedSearch initiallyToggled={toggleSidebar} searchTypeDefault={searchTypeDefault} />
      </SearchProvider>
    </>
  );
}
