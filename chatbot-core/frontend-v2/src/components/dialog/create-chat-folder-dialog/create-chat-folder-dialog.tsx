'use client';

import { useIsMutating } from '@tanstack/react-query';
import { FC } from 'react';

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { ReactMutationKey } from '@/constants/react-query-key';
import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';

import { CreateChatFolderForm } from './create-chat-folder-form';

export const CreateChatFolderDialog: FC = () => {
  const { dialogType, closeDialog } = useDialogStore();
  const isCreatingChatFolder = useIsMutating({
    mutationKey: [ReactMutationKey.CREATE_CHAT_FOLDER],
  });

  return (
    <Dialog open={dialogType === DialogType.CREATE_CHAT_FOLDER || !!isCreatingChatFolder} onOpenChange={closeDialog}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create chat folder</DialogTitle>
          <DialogDescription>Group your previous chats with EzHR using folders.</DialogDescription>
        </DialogHeader>
        <CreateChatFolderForm />
      </DialogContent>
    </Dialog>
  );
};
