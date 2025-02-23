'use client';

import { FC } from 'react';

import withDialogRender from '@/hoc/with-dialog-render';
import { DialogType } from '@/hooks/stores/use-dialog-store';

import { ConfirmationDialog } from '../confirmation-dialog';
import { SelectChatFolder } from './select-chat-folder';
import { useMoveChatSession } from './use-move-chat-session';

export const MOVE_TO_CHAT_HISTORY_VALUE = 'move-to-chat-history-value';

const MoveChatSessionDialog: FC = () => {
  const {
    isOpenDialog,
    closeDialog,
    preventClose,
    onEditChatSession,
    selectedFolder,
    setSelectedFolder,
    previousFolder,
    chatFolders,
  } = useMoveChatSession();

  return (
    <ConfirmationDialog
      title="Move chat session"
      description="Move your chat into any folders."
      isOpen={isOpenDialog}
      onConfirm={onEditChatSession}
      onClose={closeDialog}
      preventClose={preventClose}
    >
      <SelectChatFolder
        selectedFolder={selectedFolder}
        setSelectedFolder={setSelectedFolder}
        chatFolders={chatFolders}
        previousFolder={previousFolder}
      />
    </ConfirmationDialog>
  );
};

export default withDialogRender(MoveChatSessionDialog, DialogType.MOVE_CHAT_SESSION);
