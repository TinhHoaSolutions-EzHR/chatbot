'use client';
import { DndContext, DragEndEvent } from '@dnd-kit/core';
import { restrictToVerticalAxis } from '@dnd-kit/modifiers';
import React, { useState } from 'react';
import { toast } from 'sonner';

import { Sidebar, SidebarContent, SidebarFooter, SidebarSeparator } from '@/components/ui/sidebar';
import { useEditChatSession } from '@/hooks/chat/use-edit-chat-session';

import { AppSidebarHeader } from './app-sidebar-header';
import { ChatFolders } from './chat-folders/chat-folders';
import { ChatHistory } from './chat-history/chat-history';

export function AppSidebar() {
  const [, setIsDropped] = useState(false);
  const { mutate } = useEditChatSession();

  function handleDragEnd(event: DragEndEvent) {
    if (event.over) {
      setIsDropped(true);
      mutate(
        { chatSessionId: `${event.active.id}`, data: { folder_id: `${event.over.id}` } },
        {
          onSuccess() {
            toast.success('Move chat successfully!');
          },
          onError() {
            toast.error('Move chat failed.', {
              description: "There's something wrong with your request. Please try again later!",
            });
          },
        },
      );
    }
  }

  return (
    <DndContext modifiers={[restrictToVerticalAxis]} onDragEnd={handleDragEnd}>
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
