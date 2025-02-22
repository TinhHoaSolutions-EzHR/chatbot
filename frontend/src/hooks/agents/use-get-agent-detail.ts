import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getAgentDetail } from '@/services/agents/get-agent-detail';

export const useGetAgentDetail = (agentId: string) => {
  return useQuery({
    queryKey: [ReactQueryKey.AGENT, { agentId }],
    queryFn: () => getAgentDetail(agentId),
  });
};
