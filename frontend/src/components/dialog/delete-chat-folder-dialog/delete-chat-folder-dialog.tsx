'use client';

import { FC } from 'react';

import withDialogRender from '@/hoc/with-dialog-render';
import { DialogType } from '@/hooks/stores/use-dialog-store';

import { ConfirmationDialog } from '../confirmation-dialog';
import { useDeleteChatFolderHelper } from './use-delete-chat-folder-helper';

const DeleteChatFolderDialog: FC = () => {
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

export default withDialogRender(DeleteChatFolderDialog, DialogType.DELETE_CHAT_FOLDER);
