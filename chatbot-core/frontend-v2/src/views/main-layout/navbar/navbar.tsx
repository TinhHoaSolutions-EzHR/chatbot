'use client';

import { AppLogo } from '@/components/app-logo';
import { NewChatButton } from '@/components/new-chat-button';
import { SidebarTrigger, useSidebar } from '@/components/ui/sidebar';
import { UserButton } from '@/components/user-button/user-button';

import { AgentSelector } from './agent-selector/agent-selector';

export const Navbar = () => {
  const { open } = useSidebar();

  return (
    <nav className="sticky top-0 grid grid-cols-3 items-center py-2 px-2 bg-white/70 backdrop-blur-md">
      <div className="flex items-center">
        {!open && (
          <>
            <SidebarTrigger />
            <NewChatButton />
          </>
        )}
        <AppLogo />
      </div>
      <div className="place-items-center">
        <AgentSelector />
      </div>
      <div className="place-items-end">
        <UserButton />
      </div>
    </nav>
  );
};
