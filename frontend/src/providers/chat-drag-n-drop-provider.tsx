'use client';

import { DndContext, DragStartEvent, DragEndEvent } from '@dnd-kit/core';
import { restrictToVerticalAxis } from '@dnd-kit/modifiers';
import React, { FC, ReactNode, useState } from 'react';
import { toast } from 'sonner';

import { SIDEBAR_CHAT_HISTORY } from '@/constants/sidebar-items';
import { useEditChatSession } from '@/hooks/chat/use-edit-chat-session';

const useHandleDrag = () => {
  const { mutate } = useEditChatSession();
  const [initialOverId, setInitialOverId] = useState<string | null>(null); // Store the initial drop zone

  const handleDragStart = (event: DragStartEvent) => {
    setInitialOverId(event.active.data.current?.parentId ?? null); // Track the initial droppable ID
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const finalOverId = event.over?.id ?? null; // Get final drop location

    if (finalOverId === initialOverId) {
      return; // Stop execution if it's dropped in the same place
    }

    mutate(
      {
        chatSessionId: `${event.active.id}`,
        data: { folder_id: finalOverId === SIDEBAR_CHAT_HISTORY ? null : `${finalOverId}` },
      },
      {
        onSuccess() {
          toast.success('Move chat successfully!');
          setInitialOverId(null);
        },
        onError() {
          toast.error('Move chat failed.', {
            description: "There's something wrong with your request. Please try again later!",
          });
          setInitialOverId(null);
        },
      }
    );
  };

  return { handleDragStart, handleDragEnd };
};

type Props = {
  children: ReactNode;
};

const ChatSidebarDndProvider: FC<Props> = ({ children }) => {
  const { handleDragStart, handleDragEnd } = useHandleDrag();

  return (
    <DndContext
      modifiers={[restrictToVerticalAxis]}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      {children}
    </DndContext>
  );
};

export default ChatSidebarDndProvider;
