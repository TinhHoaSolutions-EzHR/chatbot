'use client';

import { useQueryClient } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { ReactNode, useEffect } from 'react';

import { ACCESS_TOKEN_LOCAL_STORAGE_EVENT_DISPATCH } from '@/constants/misc';
import { ReactQueryKey } from '@/constants/react-query-key';
import { useGetUserInfo } from '@/hooks/user/use-get-user-info';

import { OauthLogin } from './oauth-login';

type Props = {
  children: ReactNode;
};

export default function AuthProvider({ children }: Props) {
  const { data: userInfo, isLoading, isRefetching, isError } = useGetUserInfo();
  const queryClient = useQueryClient();

  // This use effect listener will listen on every changes on the local storage event for
  // changing access token.
  useEffect(() => {
    const storageListener = () => {
      queryClient.invalidateQueries({
        queryKey: [ReactQueryKey.USER],
      });
    };
    window.addEventListener(ACCESS_TOKEN_LOCAL_STORAGE_EVENT_DISPATCH, storageListener);

    return () => window.removeEventListener(ACCESS_TOKEN_LOCAL_STORAGE_EVENT_DISPATCH, storageListener);
  }, []);

  if (isLoading || (isRefetching && !userInfo)) {
    return (
      <div className="full-screen-center">
        <Loader2 className="animate-spin" size={32} />
      </div>
    );
  }

  if (isError || !userInfo) {
    return (
      <>
        <OauthLogin />
      </>
    );
  }

  return <>{children}</>;
}
