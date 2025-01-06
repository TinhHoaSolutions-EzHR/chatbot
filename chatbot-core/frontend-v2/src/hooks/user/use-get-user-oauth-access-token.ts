import { useQuery, useQueryClient } from '@tanstack/react-query';

import { ReactQueryKey } from '@/constants/react-query-key';
import { getUserOauthAccessToken } from '@/services/user/get-user-oauth-access-token';

export const useGetUserOauthAccessToken = (code?: string) => {
  const queryClient = useQueryClient();

  return useQuery({
    queryKey: [ReactQueryKey.USER_ACCESS_TOKEN, { code }],
    queryFn: async () => {
      if (!code) return undefined;

      const isSuccess = await getUserOauthAccessToken(code);

      if (isSuccess) {
        queryClient.invalidateQueries({
          queryKey: [ReactQueryKey.USER],
          refetchType: 'active',
        });
      }
    },
    enabled: !!code,
  });
};
