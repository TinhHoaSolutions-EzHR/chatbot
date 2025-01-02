import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getAgentsList } from '@/services/agents/get-agents-list';

export const useGetAgentsList = () => {
  return useQuery({
    queryKey: [ReactQueryKey.AGENTS],
    queryFn: getAgentsList,
  });
};
