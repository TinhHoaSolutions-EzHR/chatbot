import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getCurrentUser } from '@/services/user/get-current-user';

export const useGetUserInfo = () => {
  return useQuery({
    queryKey: [ReactQueryKey.USER],
    queryFn: getCurrentUser,
  });
};
