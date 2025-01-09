import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import httpClient from '@/lib/axios';

export const useApiHealthCheck = () => {
  return useQuery({
    queryKey: [ReactQueryKey.HEALTH_CHECK],
    queryFn: () => httpClient.get('/health'),
  });
};
