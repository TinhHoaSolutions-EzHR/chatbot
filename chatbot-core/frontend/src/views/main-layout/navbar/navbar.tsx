'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';

import AppLogo from '@/components/app-logo';
import { NewChatButton } from '@/components/new-chat-button';
import { SidebarTrigger, useSidebar } from '@/components/ui/sidebar';
import { UserButton } from '@/components/user-button/user-button';
import WillRender from '@/components/will-render';
import { Route } from '@/constants/misc';

import { AgentSelector } from './agent-selector/agent-selector';

export const Navbar = () => {
  const { open } = useSidebar();
  const router = useRouter();

  return (
    <nav className="sticky top-0 grid grid-cols-3 items-center py-2 px-2">
      <div className="flex items-center">
        <WillRender when={!open}>
          <SidebarTrigger />
          <NewChatButton onClick={() => router.push(Route.HOME_PAGE)} />
        </WillRender>
        <Link href={Route.HOME_PAGE}>
          <AppLogo className="w-28" />
        </Link>
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
