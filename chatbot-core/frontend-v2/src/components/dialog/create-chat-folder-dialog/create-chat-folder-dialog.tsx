'use client';

import { Loader2 } from 'lucide-react';
import { FC } from 'react';

import { Button } from '@/components/ui/button';
import { DialogFooter } from '@/components/ui/dialog';
import withDialogRender from '@/hoc/with-dialog-render';
import { DialogType } from '@/hooks/stores/use-dialog-store';

import { ConfirmationDialog } from '../confirmation-dialog';
import { CreateChatFolderForm } from './create-chat-folder-form';
import { useCreateFolderHelper } from './use-create-folder-helper';

const CreateChatFolderDialog: FC = () => {
  const { isOpenDialog, closeDialog, onCreateChatFolder, preventClose } = useCreateFolderHelper();

  return (
    <ConfirmationDialog
      isOpen={isOpenDialog}
      onClose={closeDialog}
      title="Create chat folder"
      description="Group your previous chats with EzHR using folders."
      preventClose={preventClose}
      customFooter
    >
      <CreateChatFolderForm onCreateChatFolder={onCreateChatFolder}>
        <DialogFooter className="mt-6">
          <Button type="submit" disabled={preventClose}>
            {preventClose ? <Loader2 className="animate-spin" size={14} /> : 'Submit'}
          </Button>
          <Button variant="secondary" onClick={closeDialog} disabled={preventClose}>
            Cancel
          </Button>
        </DialogFooter>
      </CreateChatFolderForm>
    </ConfirmationDialog>
  );
};

export default withDialogRender(CreateChatFolderDialog, DialogType.CREATE_CHAT_FOLDER);
