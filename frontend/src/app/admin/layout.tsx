import { ReactNode } from 'react';

import AdminRequiredProvider from '@/providers/admin-required-provider';
import AdminLayoutView from '@/views/admin-layout/admin-layout';

type Props = {
  children: ReactNode;
};

export default function AdminLayout({ children }: Props) {
  return (
    <AdminRequiredProvider>
      <AdminLayoutView>{children}</AdminLayoutView>
    </AdminRequiredProvider>
  );
}
