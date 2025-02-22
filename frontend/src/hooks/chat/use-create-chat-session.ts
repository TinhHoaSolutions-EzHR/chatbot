import { useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactMutationKey, ReactQueryKey } from '@/constants/react-query-key';
import { createChatSession } from '@/services/chat/create-chat-session';
import { IChatSession, IChatSessionDetail } from '@/types/chat';

export const useCreateChatSession = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: [ReactMutationKey.CREATE_CHAT_SESSION],
    mutationFn: createChatSession,
    onSuccess(newData) {
      queryClient.setQueryData([ReactQueryKey.CHAT_SESSIONS], (oldData?: IChatSession[]) =>
        oldData ? [newData, ...oldData] : [newData],
      );
      queryClient.setQueryData([ReactQueryKey.CHAT_SESSION, { chatSessionId: newData.id }], () => {
        const newChatSessionDetail: IChatSessionDetail = {
          ...newData,
          chat_messages: [],
        };

        return newChatSessionDetail;
      });
    },
  });
};
