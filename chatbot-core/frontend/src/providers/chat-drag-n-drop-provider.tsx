'use client';
import { DndContext, DragEndEvent } from '@dnd-kit/core';
import { restrictToVerticalAxis } from '@dnd-kit/modifiers';
import React, { FC, ReactNode } from 'react';
import { toast } from 'sonner';

import { SIDEBAR_CHAT_HISTORY } from '@/constants/sidebar-items';
import { useEditChatSession } from '@/hooks/chat/use-edit-chat-session';

const useHandleDragEnd = () => {
  const { mutate } = useEditChatSession();

  return (event: DragEndEvent) => {
    if (event.over) {
      mutate(
        {
          chatSessionId: `${event.active.id}`,
          data: { folder_id: `${event.over.id}` === SIDEBAR_CHAT_HISTORY ? null : `${event.over.id}` },
        },
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
  };
};

type Props = {
  children: ReactNode;
};

const ChatSidebarDndProvider: FC<Props> = ({ children }) => {
  const handleDragEnd = useHandleDragEnd();

  return (
    <DndContext modifiers={[restrictToVerticalAxis]} onDragEnd={handleDragEnd}>
      {children}
    </DndContext>
  );
};

export default ChatSidebarDndProvider;
