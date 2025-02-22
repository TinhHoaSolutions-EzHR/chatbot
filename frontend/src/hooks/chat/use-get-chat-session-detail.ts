import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getChatSessionDetail } from '@/services/chat/get-chat-session-detail';

export const useGetChatSessionDetail = (chatSessionId: string | null | undefined) => {
  return useQuery({
    queryKey: [ReactQueryKey.CHAT_SESSION, { chatSessionId }],
    queryFn: async () => {
      if (!chatSessionId) {
        // Should not go here
        throw new Error('Chat session id not found');
      }

      return getChatSessionDetail(chatSessionId);
    },
    enabled: !!chatSessionId,
  });
};
