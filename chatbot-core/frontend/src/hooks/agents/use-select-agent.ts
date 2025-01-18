import { useMutation, useQueryClient } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { selectAgent } from '@/services/agents/select-agent';

export const useSelectAgent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: selectAgent,
    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: [ReactQueryKey.USER_SETTINGS],
      });
    },
  });
};
