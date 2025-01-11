import { DndContext } from '@dnd-kit/core';
import { FC, ReactNode } from 'react';

import { DND_CHAT_HISTORY_ID } from '@/constants/misc';
import { useEditChatSession } from '@/hooks/chat/use-edit-chat-session';

type Props = {
  children: ReactNode;
};

const FoldersDndProvider: FC<Props> = ({ children }) => {
  const { mutate } = useEditChatSession();

  return (
    <DndContext
      onDragEnd={e => {
        if (!e.over || !e.active || e.over.id.toString() === e.active.id.toString()) {
          return;
        }

        const isAddChatToFolder = e.over.id.toString() !== DND_CHAT_HISTORY_ID;
        const folderId = isAddChatToFolder ? e.over.id.toString() : null;

        mutate({
          chatSessionId: e.active.id.toString(),
          data: {
            folder_id: folderId,
          },
        });
      }}
    >
      {children}
    </DndContext>
  );
};

export default FoldersDndProvider;
