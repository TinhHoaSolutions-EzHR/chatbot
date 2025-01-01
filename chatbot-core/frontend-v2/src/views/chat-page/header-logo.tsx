'use client';

import { AppLogo } from '@/components/app-logo';
import { NewChatButton } from '@/components/new-chat-button';
import { SidebarTrigger, useSidebar } from '@/components/ui/sidebar';

export const HeaderLogo = () => {
  const { open } = useSidebar();

  return (
    <div className="flex items-center py-2 px-2">
      {!open && (
        <>
          <SidebarTrigger />
          <NewChatButton />
        </>
      )}
      <AppLogo />
    </div>
  );
};
