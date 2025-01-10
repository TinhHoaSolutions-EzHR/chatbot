import { useMutation } from '@tanstack/react-query';

import { ReactMutationKey } from '@/constants/react-query-key';
import { createChatMessage } from '@/services/chat/create-chat-message';
import { IChatMessageRequest } from '@/types/chat';

export const useCreateChatMessage = (chatSessionId?: string, data?: Partial<IChatMessageRequest>) => {
  return useMutation({
    mutationKey: [ReactMutationKey.CREATE_CHAT_MESSAGE],
    mutationFn: async () => {
      if (!chatSessionId || !data) {
        return;
      }

      await createChatMessage(chatSessionId, data);
    },
  });
};
