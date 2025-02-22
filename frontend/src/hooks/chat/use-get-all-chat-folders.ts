import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getAllChatFolders } from '@/services/chat/get-all-chat-folders';

export const useGetAllChatFolders = () => {
  return useQuery({
    queryKey: [ReactQueryKey.CHAT_FOLDERS],
    queryFn: getAllChatFolders,
  });
};
