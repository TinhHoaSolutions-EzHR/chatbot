'use client';

import { Loader2 } from 'lucide-react';
import { ReactNode } from 'react';

import { useGetUserInfo } from '@/hooks/user/use-get-user-info';

import { OauthLogin } from './oauth-login';

type Props = {
  children: ReactNode;
};

export default function AuthProvider({ children }: Props) {
  const { data: userInfo, isLoading, isRefetching, isError } = useGetUserInfo();

  if (isLoading || isRefetching) {
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
