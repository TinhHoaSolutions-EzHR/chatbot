import { useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactMutationKey, ReactQueryKey } from '@/constants/react-query-key';
import { createChatFolder } from '@/services/chat/create-chat-folder';
import { IFolder } from '@/types/chat';

export const useCreateChatFolder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createChatFolder,
    mutationKey: [ReactMutationKey.CREATE_CHAT_FOLDER],
    onSuccess(data) {
      queryClient.setQueryData([ReactQueryKey.CHAT_FOLDERS], (oldData?: IFolder[]) =>
        oldData ? [data, ...oldData] : [data],
      );
    },
  });
};
