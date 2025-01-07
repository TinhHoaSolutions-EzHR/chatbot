import { useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';

import { LOCAL_STORAGE_ACCESS_TOKEN_KEY } from '@/configs/misc';

export const useUserLogout = () => {
  const queryClient = useQueryClient();
  const router = useRouter();

  return () => {
    localStorage.removeItem(LOCAL_STORAGE_ACCESS_TOKEN_KEY);
    queryClient.invalidateQueries({
      type: 'active',
    });
    router.push('/');
  };
};
