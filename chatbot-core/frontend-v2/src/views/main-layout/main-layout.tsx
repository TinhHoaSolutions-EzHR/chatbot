import { ReactNode } from 'react';

import { SidebarProvider } from '@/components/ui/sidebar';

import { AppSidebar } from './app-sidebar';
import { ChatBox } from './chat-box/chat-box';
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
        <div className="relative w-full flex-1 flex flex-col">
          <div className="absolute inset-0 bottom-[130px] overflow-auto grid place-items-center">{children}</div>
          <div className="absolute bottom-0 left-0 right-0 flex justify-center px-4">
            <ChatBox />
          </div>
        </div>
      </main>
    </SidebarProvider>
  );
}
