import { toast } from 'sonner';

import { useDeleteChatSession } from '@/hooks/chat/use-delete-chat-session';
import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';

export const useDeleteChatSessionHelper = () => {
  const { dialogType, data, closeDialog } = useDialogStore();
  const { chatSession } = data || {};

  const { mutate, isPending } = useDeleteChatSession(chatSession?.id);

  const onDeleteChatSession = () => {
    if (!chatSession) {
      toast.error('Something went wrong!', {
        description: 'Please try again later.',
      });
      return;
    }

    mutate(chatSession.id, {
      onSuccess() {
        toast.success('Delete chat session successfully.');
        closeDialog();
      },
      onError() {
        toast.error('Delete chat session failed', {
          description: "There's something wrong with your request. Please try again later.",
        });
      },
    });
  };

  return {
    isOpenDialog: dialogType === DialogType.DELETE_CHAT_SESSION,
    closeDialog,
    onDeleteChatSession,
    preventClose: isPending,
  };
};
