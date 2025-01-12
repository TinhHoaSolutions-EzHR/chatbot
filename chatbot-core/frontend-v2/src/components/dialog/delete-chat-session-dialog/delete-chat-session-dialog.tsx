'use client';

import { FC } from 'react';

import { ConfirmationDialog } from '../confirmation-dialog';
import { useDeleteChatSessionHelper } from './use-delete-chat-session-helper';

export const DeleteChatSessionDialog: FC = () => {
  const { isOpenDialog, closeDialog, onDeleteChatSession, preventClose } = useDeleteChatSessionHelper();

  return (
    <ConfirmationDialog
      isOpen={isOpenDialog}
      onClose={closeDialog}
      title="Are you sure"
      description="You are about to delete this chat session."
      onConfirm={onDeleteChatSession}
      preventClose={preventClose}
    />
  );
};
