import { useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactMutationKey, ReactQueryKey } from '@/constants/react-query-key';
import { deleteChatFolder } from '@/services/chat/delete-chat-folder';
import { IFolder } from '@/types/chat';

export const useDeleteChatFolder = (folderId?: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteChatFolder,
    mutationKey: [ReactMutationKey.DELETE_CHAT_FOLDER, { id: folderId }],
    onSuccess(_, variables) {
      queryClient.setQueryData([ReactQueryKey.CHAT_FOLDERS], (oldData?: IFolder[]) =>
        oldData ? oldData.filter(value => value.id !== variables) : oldData,
      );
    },
  });
};
