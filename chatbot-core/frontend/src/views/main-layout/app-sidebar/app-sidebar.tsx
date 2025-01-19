'use client';

import { Sidebar, SidebarContent, SidebarFooter, SidebarSeparator } from '@/components/ui/sidebar';

import { AppSidebarHeader } from './app-sidebar-header';
import { ChatFolders } from './chat-folders/chat-folders';
import { ChatHistory } from './chat-history/chat-history';

export function AppSidebar() {
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
