'use client';

import { AppLogo } from '@/components/app-logo';
import { NewChatButton } from '@/components/new-chat-button';
import { SidebarTrigger, useSidebar } from '@/components/ui/sidebar';

import { UserButton } from './user-button/user-button';

export const HeaderLogo = () => {
  const { open } = useSidebar();

  return (
    <div className="flex items-center justify-between py-2 px-2">
      <div className="flex items-center">
        {!open && (
          <>
            <SidebarTrigger />
            <NewChatButton />
          </>
        )}
        <AppLogo />
      </div>
      <UserButton />
    </div>
  );
};
