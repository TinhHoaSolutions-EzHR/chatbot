import { useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactMutationKey, ReactQueryKey } from '@/constants/react-query-key';
import { deleteChatSession } from '@/services/chat/delete-chat-session';
import { IChatSession } from '@/types/chat';

export const useDeleteChatSession = (chatSessionId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: [ReactMutationKey.DELETE_CHAT_SESSION, { id: chatSessionId }],
    mutationFn: () => deleteChatSession(chatSessionId),
    onSuccess() {
      queryClient.setQueryData([ReactQueryKey.CHAT_SESSIONS], (oldData?: IChatSession[]) =>
        oldData ? oldData.filter(chatSession => chatSession.id !== chatSessionId) : oldData,
      );
    },
  });
};
