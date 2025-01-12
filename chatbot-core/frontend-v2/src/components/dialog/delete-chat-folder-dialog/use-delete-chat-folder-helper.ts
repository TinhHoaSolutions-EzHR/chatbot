import { toast } from 'sonner';

import { useDeleteChatFolder } from '@/hooks/chat/use-delete-chat-folder';
import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';

export const useDeleteChatFolderHelper = () => {
  const { dialogType, closeDialog, data } = useDialogStore();
  const { folder } = data || {};

  const { mutate, isPending } = useDeleteChatFolder(folder?.id);

  const onDeleteChatFolder = () => {
    if (!folder?.id) {
      toast.error('Something went wrong', {
        description: 'Please try again later.',
      });
      return;
    }

    mutate(folder.id, {
      onSuccess() {
        toast.success('Delete chat folder successfully');
        closeDialog();
      },
      onError() {
        toast.error('Delete chat folder failed', {
          description: "There's something wrong with your request. Please try again later!",
        });
      },
    });
  };

  return {
    isOpenDialog: dialogType === DialogType.DELETE_CHAT_FOLDER,
    closeDialog,
    onDeleteChatFolder,
    preventClose: isPending,
  };
};
