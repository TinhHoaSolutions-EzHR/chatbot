import { useSearchParams } from 'next/navigation';

export default function ChatPageView() {
  const searchParams = useSearchParams();

  const data = await fetchChatData(searchParams);

  if ('redirect' in data) {
    redirect(data.redirect);
  }

  const {
    user,
    chatSessions,
    availableSources,
    documentSets,
    tags,
    llmProviders,
    folders,
    toggleSidebar,
    openedFolders,
    defaultAssistantId,
    shouldShowWelcomeModal,
    userInputPrompts,
  } = data;

  return (
    <>
      <InstantSSRAutoRefresh />
      {shouldShowWelcomeModal && <WelcomeModal user={user} requestCookies={requestCookies} />}
      <ChatProvider
        value={{
          chatSessions,
          availableSources,
          availableDocumentSets: documentSets,
          availableTags: tags,
          llmProviders,
          folders,
          openedFolders,
          userInputPrompts,
          shouldShowWelcomeModal,
          defaultAssistantId,
        }}
      >
        <WrappedChat initiallyToggled={toggleSidebar} />
      </ChatProvider>
    </>
  );
}
