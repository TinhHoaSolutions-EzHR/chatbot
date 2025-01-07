import { useQuery, useQueryClient } from '@tanstack/react-query';

import { LOCAL_STORAGE_ACCESS_TOKEN_KEY } from '@/configs/misc';
import { ReactQueryKey } from '@/constants/react-query-key';
import { getUserOauthAccessToken } from '@/services/user/get-user-oauth-access-token';

export const useGetUserOauthAccessToken = (code?: string) => {
  const queryClient = useQueryClient();

  return useQuery({
    queryKey: [ReactQueryKey.USER_ACCESS_TOKEN, { code }],
    queryFn: async () => {
      if (!code) return undefined;

      const { access_token } = await getUserOauthAccessToken(code);

      localStorage.setItem(LOCAL_STORAGE_ACCESS_TOKEN_KEY, access_token);

      queryClient.invalidateQueries({
        queryKey: [ReactQueryKey.USER],
        refetchType: 'active',
      });
    },
    enabled: !!code,
  });
};
