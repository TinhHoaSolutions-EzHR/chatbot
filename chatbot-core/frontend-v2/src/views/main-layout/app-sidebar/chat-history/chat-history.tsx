import { FC } from 'react';

import { SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarMenu } from '@/components/ui/sidebar';

export const ChatHistory: FC = () => {
  return (
    <>
      <h3 className="text-xs font-bold text-zinc-600 ml-4 mt-2">History</h3>
      <SidebarGroup>
        <SidebarGroupLabel>Today</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu></SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </>
  );
};
