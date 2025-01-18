'use client';

import { FC } from 'react';

import withDialogRender from '@/hoc/with-dialog-render';
import { DialogType } from '@/hooks/stores/use-dialog-store';

import { ConfirmationDialog } from '../confirmation-dialog';
import { useDeleteChatSessionHelper } from './use-delete-chat-session-helper';

const DeleteChatSessionDialog: FC = () => {
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

export default withDialogRender(DeleteChatSessionDialog, DialogType.DELETE_CHAT_SESSION);
