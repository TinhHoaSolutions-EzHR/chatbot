import { toast } from 'sonner';

import { useCreateChatFolder } from '@/hooks/chat/use-create-chat-folder';
import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';

export const useCreateFolderHelper = () => {
  const dialogType = useDialogStore(state => state.dialogType);
  const closeDialog = useDialogStore(state => state.closeDialog);

  const { mutate, isPending } = useCreateChatFolder();

  const onCreateChatFolder = (folderName: string) => {
    mutate(folderName, {
      onSuccess() {
        toast.success('Folder created successfully!');
        closeDialog();
      },
      onError() {
        toast.error('Folder created unsuccessfully!', {
          description: 'Please try again later.',
        });
      },
    });
  };

  return {
    isOpenDialog: dialogType === DialogType.CREATE_CHAT_FOLDER,
    closeDialog,
    onCreateChatFolder,
    preventClose: isPending,
  };
};
