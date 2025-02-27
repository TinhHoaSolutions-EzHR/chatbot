import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getIndexStatus } from '@/services/documents/get-index-status';
import { IndexStatus } from '@/types/document';

const INDEX_STATUS_REFETCH_INTERVAL = 5000;

export const useGetIndexStatus = (taskId: string | undefined) => {
  return useQuery({
    queryKey: [ReactQueryKey.GET_INDEX_STATUS, taskId],
    queryFn: () => {
      if (!taskId) {
        return;
      }

      return getIndexStatus(taskId);
    },
    enabled: !!taskId,
    refetchInterval: data => {
      if (!data.state.data) {
        return INDEX_STATUS_REFETCH_INTERVAL;
      }

      if ([IndexStatus.SUCCESS, IndexStatus.FAILURE].includes(data.state.data.status)) {
        return false;
      }

      return INDEX_STATUS_REFETCH_INTERVAL;
    },
  });
};
