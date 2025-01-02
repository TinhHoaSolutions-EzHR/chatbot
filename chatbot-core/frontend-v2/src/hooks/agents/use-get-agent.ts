import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getAgent } from '@/services/agents/get-agent';

export const useGetAgent = (agentId: string | undefined) => {
  return useQuery({
    queryKey: [ReactQueryKey.AGENT, { agentId }],
    queryFn: async () => {
      if (!agentId) {
        return null;
      }

      return await getAgent(agentId);
    },
    enabled: !!agentId,
  });
};
