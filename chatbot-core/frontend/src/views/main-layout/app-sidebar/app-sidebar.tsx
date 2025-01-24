'use client';
import React from 'react';

import { Sidebar, SidebarContent, SidebarFooter, SidebarSeparator } from '@/components/ui/sidebar';
import ChatSidebarDndProvider from '@/providers/chat-drag-n-drop-provider';

import { AppSidebarHeader } from './app-sidebar-header';
import { ChatFolders } from './chat-folders/chat-folders';
import { ChatHistory } from './chat-history/chat-history';

export function AppSidebar() {
  return (
    <Sidebar>
      <AppSidebarHeader />
      <SidebarSeparator className="mt-1" />
      <ChatSidebarDndProvider>
        <SidebarContent>
          <ChatFolders />
          <SidebarSeparator />
          <ChatHistory />
        </SidebarContent>
      </ChatSidebarDndProvider>
      <SidebarFooter />
    </Sidebar>
  );
}
