'use client';

import { ReactNode } from 'react';

import { SidebarProvider } from '@/components/ui/sidebar';
import { UserButton } from '@/components/user-button/user-button';

import { AdminSidebar } from './admin-sidebar/admin-sidebar';

type Props = {
  children: ReactNode;
};

export default function AdminLayoutView({ children }: Props) {
  return (
    <SidebarProvider open={true}>
      <AdminSidebar />
      <main className="pt-20 pl-10 pr-14 w-full">{children}</main>
      <div className="fixed top-2 right-2">
        <UserButton />
      </div>
    </SidebarProvider>
  );
}
