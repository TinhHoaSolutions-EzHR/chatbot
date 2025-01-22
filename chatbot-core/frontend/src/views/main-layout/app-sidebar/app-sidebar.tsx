'use client';
import React from 'react';

import { Sidebar, SidebarContent, SidebarFooter, SidebarSeparator } from '@/components/ui/sidebar';
import DndContextProvider from '@/providers/drag-n-drop-provider';

import { AppSidebarHeader } from './app-sidebar-header';
import { ChatFolders } from './chat-folders/chat-folders';
import { ChatHistory } from './chat-history/chat-history';

export function AppSidebar() {
  return (
    <Sidebar>
      <AppSidebarHeader />
      <SidebarSeparator className="mt-1" />
      <DndContextProvider>
        <SidebarContent>
          <ChatFolders />
          <SidebarSeparator />
          <ChatHistory />
        </SidebarContent>
      </DndContextProvider>
      <SidebarFooter />
    </Sidebar>
  );
}
