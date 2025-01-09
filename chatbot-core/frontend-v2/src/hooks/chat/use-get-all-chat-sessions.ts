import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getAllChatSessions } from '@/services/chat/get-all-chat-sessions';

export const useGetAllChatSessions = () => {
  return useQuery({
    queryKey: [ReactQueryKey.CHAT_SESSIONS],
    queryFn: async () => {
      const chatSessions = getAllChatSessions();

      return chatSessions;
    },
  });
};
