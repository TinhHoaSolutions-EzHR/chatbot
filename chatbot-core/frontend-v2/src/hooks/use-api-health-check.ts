import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getHealthCheckUrl } from '@/utils/get-api-url';

export const useApiHealthCheck = () => {
  return useQuery({
    queryKey: [ReactQueryKey.HEALTH_CHECK],
    queryFn: () => axios.get(getHealthCheckUrl()),
  });
};
