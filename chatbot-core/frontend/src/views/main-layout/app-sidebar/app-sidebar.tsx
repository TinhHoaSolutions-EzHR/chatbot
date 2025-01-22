'use client';
import { DndContext } from '@dnd-kit/core';
import { restrictToVerticalAxis } from '@dnd-kit/modifiers';

import { Sidebar, SidebarContent, SidebarFooter, SidebarSeparator } from '@/components/ui/sidebar';

import { AppSidebarHeader } from './app-sidebar-header';
import { ChatFolders } from './chat-folders/chat-folders';
import { ChatHistory } from './chat-history/chat-history';

export function AppSidebar() {
  return (
    <DndContext modifiers={[restrictToVerticalAxis]}>
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
    </DndContext>
  );
}
