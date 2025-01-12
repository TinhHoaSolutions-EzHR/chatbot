'use client';

import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';

import { Separator } from '@/components/ui/separator';
import { SidebarProvider } from '@/components/ui/sidebar';
import { UserButton } from '@/components/user-button/user-button';
import { ADMIN_ITEM_DETAIL } from '@/constants/admin-sidebar-items';

import { AdminSidebar } from './admin-sidebar/admin-sidebar';

type Props = {
  children: ReactNode;
};

export default function AdminLayoutView({ children }: Props) {
  const pathname = usePathname();

  const pageInfo = ADMIN_ITEM_DETAIL[pathname];
  const Icon = pageInfo?.icon;

  return (
    <SidebarProvider open={true}>
      <AdminSidebar />
      {!pageInfo ? (
        <div>Something went wrong</div>
      ) : (
        <main className="pt-20 pl-10 pr-14 w-full">
          <div className="flex gap-2 items-center">
            <Icon size={30} />
            <h1 className="text-3xl font-bold">{pageInfo.name}</h1>
          </div>
          <Separator className="my-4" />
          {children}
        </main>
      )}
      <div className="fixed top-2 right-2">
        <UserButton />
      </div>
    </SidebarProvider>
  );
}
