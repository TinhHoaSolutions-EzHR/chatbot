import { ReactNode } from 'react';

import { AppSidebar } from './app-sidebar';
import { SidebarProvider } from '@/components/ui/sidebar';

type Props = {
  children: ReactNode;
};

export default function MainLayoutView({ children }: Props) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main className="w-full min-h-dvh relative">{children}</main>
    </SidebarProvider>
  );
}
