import { useQuery } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getUserSettings } from '@/services/user/get-user-settings';

export const useGetUserSettings = () => {
  return useQuery({
    queryKey: [ReactQueryKey.USER_SETTINGS],
    queryFn: getUserSettings,
  });
};
