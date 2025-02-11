'use client';
import { DndContext, DragEndEvent, UniqueIdentifier, useDndContext } from '@dnd-kit/core';
import { restrictToVerticalAxis } from '@dnd-kit/modifiers';
import React, { FC, ReactNode, useState } from 'react';
import { toast } from 'sonner';

import { SIDEBAR_CHAT_HISTORY } from '@/constants/sidebar-items';
import { useEditChatSession } from '@/hooks/chat/use-edit-chat-session';

const useHandleDragStart = () => {
  const { over } = useDndContext();
  const [previousOver, setPreviousOver] = useState<UniqueIdentifier | null>(null);
  return () => {
    if (previousOver) {
      toast.error('Move chat failed.', {
        description: "There's something wrong with your request. Please try again later!",
      });
    }
    setPreviousOver(over?.id ?? null);
  };
};

const useHandleDragEnd = () => {
  const { mutate } = useEditChatSession();
  const [previousOver] = useState<UniqueIdentifier | null>(null);

  return (event: DragEndEvent) => {
    if (event.over !== null && event.over.id != previousOver) {
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
    <DndContext modifiers={[restrictToVerticalAxis]} onDragEnd={handleDragEnd} onDragStart={useHandleDragStart}>
      {children}
    </DndContext>
  );
};

export default ChatSidebarDndProvider;
