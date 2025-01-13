import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getAllConnectors } from '@/services/connectors/get-all-connectors';

export const useGetAllConnectors = () => {
  return useQuery({
    queryKey: [ReactQueryKey.CONNECTORS],
    queryFn: getAllConnectors,
  });
};
