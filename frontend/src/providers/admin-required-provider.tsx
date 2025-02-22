'use client';

import { Loader2 } from 'lucide-react';
import { FC, ReactNode } from 'react';

import { useGetUserInfo } from '@/hooks/user/use-get-user-info';
import { UserRole } from '@/types/user';

type Props = {
  children: ReactNode;
};

const AdminRequiredProvider: FC<Props> = ({ children }) => {
  const { data: user, isLoading } = useGetUserInfo();

  if (isLoading || !user) {
    return (
      <div className="full-screen-center">
        <Loader2 className="w-32" />
      </div>
    );
  }

  if (user.role !== UserRole.ADMIN) {
    return <div className="full-screen-center">You don't have permission to access this page</div>;
  }

  return <>{children}</>;
};

export default AdminRequiredProvider;
