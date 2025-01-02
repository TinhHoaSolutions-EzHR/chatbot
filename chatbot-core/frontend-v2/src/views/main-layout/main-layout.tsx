import { ReactNode } from 'react';

import { SidebarProvider } from '@/components/ui/sidebar';

import { AppSidebar } from './app-sidebar';
import { Navbar } from './navbar/navbar';

type Props = {
  children: ReactNode;
};

export default function MainLayoutView({ children }: Props) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main className="w-full h-dvh relative flex flex-col">
        <Navbar />
        {children}
      </main>
    </SidebarProvider>
  );
}
