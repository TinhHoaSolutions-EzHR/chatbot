import { useEffect, useState } from 'react';
import { toast } from 'sonner';

import { useEditChatSession } from '@/hooks/chat/use-edit-chat-session';
import { useGetAllChatFolders } from '@/hooks/chat/use-get-all-chat-folders';
import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';

import { MOVE_TO_CHAT_HISTORY_VALUE } from './move-chat-session-dialog';

export const useMoveChatSession = () => {
  const { dialogType, closeDialog, data } = useDialogStore();
  const [selectedFolder, setSelectedFolder] = useState('');

  const { chatSession } = data || {};

  const { mutate, isPending } = useEditChatSession();
  const { data: chatFolders } = useGetAllChatFolders();

  const previousFolder = chatSession?.folder_id
    ? chatFolders?.find(folder => folder.id === chatSession?.folder_id)
    : null;

  useEffect(() => {
    if (dialogType === DialogType.MOVE_CHAT_SESSION) {
      setSelectedFolder(previousFolder?.id ?? '');
    }
  }, [previousFolder, dialogType]);

  const onEditChatSession = () => {
    if (!chatSession) {
      return;
    }

    const folderId = selectedFolder === MOVE_TO_CHAT_HISTORY_VALUE ? null : selectedFolder;

    if (folderId === chatSession.folder_id) {
      closeDialog();
      return;
    }

    mutate(
      { chatSessionId: chatSession.id, data: { folder_id: folderId } },
      {
        onSuccess() {
          toast.success('Move chat successfully!');
          closeDialog();
        },
        onError() {
          toast.error('Move chat failed.', {
            description: "There's something wrong with your request. Please try again later!",
          });
        },
      },
    );
  };

  return {
    selectedFolder,
    setSelectedFolder,
    previousFolder,
    chatFolders,
    onEditChatSession,
    preventClose: isPending,
    isOpenDialog: dialogType === DialogType.MOVE_CHAT_SESSION,
    closeDialog,
  };
};
