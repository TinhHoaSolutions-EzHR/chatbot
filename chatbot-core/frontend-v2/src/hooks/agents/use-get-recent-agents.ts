import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getRecentAgents } from '@/services/agents/get-recent-agents';

export const useGetRecentAgents = () => {
  return useQuery({
    queryKey: [ReactQueryKey.RECENT_AGENTS],
    queryFn: getRecentAgents,
  });
};
