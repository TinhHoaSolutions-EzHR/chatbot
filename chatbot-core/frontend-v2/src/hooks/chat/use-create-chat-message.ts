import { useMutation } from '@tanstack/react-query';

import { ReactMutationKey } from '@/constants/react-query-key';
import { createChatMessage } from '@/services/chat/create-chat-message';

export const useCreateChatMessage = () => {
  return useMutation({
    mutationKey: [ReactMutationKey.CREATE_CHAT_MESSAGE],
    mutationFn: createChatMessage,
  });
};
