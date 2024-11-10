"use client";

import { InstantSSRAutoRefresh } from "@/components/SSRAutoRefresh";
import { fetchChatData } from "@/lib/chat/fetchChatData";
import { redirect } from "next/navigation";
import WrappedAssistantsMine from "./WrappedAssistantsMine";
import { WelcomeModal } from "@/components/initialSetup/welcome/WelcomeModalWrapper";
import Cookies from "js-cookie";

export default async function GalleryPage(props: {
  searchParams: Promise<{ [key: string]: string }>;
}) {
  // Retrieve cookies on the client side using js-cookie
  const requestCookies = Cookies.get(); // This gives you an object: { [key: string]: string }

  // Resolve the search params
  const searchParams = await props.searchParams;

  // Fetch data based on the search params
  const data = await fetchChatData(searchParams);

  // Redirect if the data contains a redirect URL
  if ("redirect" in data) {
    redirect(data.redirect);
  }

  // Destructure the data
  const {
    user,
    chatSessions,
    folders,
    openedFolders,
    toggleSidebar,
    shouldShowWelcomeModal,
  } = data;

  return (
    <>
      {shouldShowWelcomeModal && (
        <WelcomeModal user={user} requestCookies={requestCookies} />
      )}

      <InstantSSRAutoRefresh />

      <WrappedAssistantsMine
        initiallyToggled={toggleSidebar}
        chatSessions={chatSessions}
        folders={folders}
        openedFolders={openedFolders}
      />
    </>
  );
}
