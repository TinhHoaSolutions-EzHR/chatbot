import { ReactQueryKey } from '@/constants/query-key';
import { getAuthTypeMetadata } from '@/services/auth/auth-type';
import { useQuery } from '@tanstack/react-query';

export const useGetAuthType = () => {
  return useQuery({
    queryKey: [ReactQueryKey.AUTH_TYPE],
    queryFn: async () => await getAuthTypeMetadata(),
  });
};
