import { useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { createChatFolder } from '@/services/chat/create-chat-folder';
import { IFolder } from '@/types/chat';

export const useCreateChatFolder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createChatFolder,
    onSuccess(data) {
      queryClient.setQueryData([ReactQueryKey.CHAT_FOLDERS], (oldData?: IFolder[]) =>
        oldData ? [data, ...oldData] : [data],
      );
    },
  });
};
