import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getAgentsList } from '@/services/agents/get-agents-list';
import { IAgent } from '@/types/agent';

export const useGetAgentsList = () => {
  return useQuery({
    queryKey: [ReactQueryKey.AGENTS],
    queryFn: async () => {
      const agentsList = await getAgentsList();

      return {
        agentsList,
        mappedAgentsById: agentsList.reduce<Record<string, IAgent>>((acc, cur) => {
          acc[cur.id] = cur;
          return acc;
        }, {}),
      };
    },
  });
};
