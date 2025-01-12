'use client';

import { FC } from 'react';

import { ConfirmationDialog } from '../confirmation-dialog';
import { useDeleteChatFolderHelper } from './use-delete-chat-folder-helper';

export const DeleteChatFolderDialog: FC = () => {
  const { isOpenDialog, closeDialog, onDeleteChatFolder, preventClose } = useDeleteChatFolderHelper();

  return (
    <ConfirmationDialog
      isOpen={isOpenDialog}
      onClose={closeDialog}
      onConfirm={onDeleteChatFolder}
      title="Are you sure?"
      description="You are about to delete this folder along with its chats."
      preventClose={preventClose}
    />
  );
};
