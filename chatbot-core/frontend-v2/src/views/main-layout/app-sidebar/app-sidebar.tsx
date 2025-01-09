'use client';

import { useMemo } from 'react';

import { Sidebar, SidebarContent, SidebarFooter, SidebarSeparator } from '@/components/ui/sidebar';
import { useGetAllChatSessions } from '@/hooks/chat/use-get-all-chat-sessions';
import { groupChatSessions } from '@/utils/group-chat-sessions';

import { AppSidebarHeader } from './app-sidebar-header';
import { ChatFolders } from './chat-folders/chat-folders';
import { ChatHistory } from './chat-history/chat-history';

export function AppSidebar() {
  const { data: chatSessions } = useGetAllChatSessions();

  const groupedChatSessions = useMemo(
    () => (chatSessions ? groupChatSessions(chatSessions) : undefined),
    [chatSessions],
  );

  console.error(groupedChatSessions);

  return (
    <Sidebar>
      <AppSidebarHeader />
      <SidebarSeparator className="mt-1" />
      <SidebarContent>
        <ChatFolders />
        <SidebarSeparator />
        <ChatHistory />
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
}
