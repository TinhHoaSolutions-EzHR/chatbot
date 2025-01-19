import { useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactMutationKey, ReactQueryKey } from '@/constants/react-query-key';
import { createChatSession } from '@/services/chat/create-chat-session';
import { IChatSession } from '@/types/chat';

export const useCreateChatSession = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: [ReactMutationKey.CREATE_CHAT_SESSION],
    mutationFn: createChatSession,
    onSuccess(data) {
      queryClient.setQueryData([ReactQueryKey.CHAT_SESSIONS], (oldData?: IChatSession[]) =>
        oldData ? [data, ...oldData] : [data],
      );
    },
  });
};
