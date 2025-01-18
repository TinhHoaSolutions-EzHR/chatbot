import { FC, ReactNode } from 'react';

import { SidebarGroup, SidebarGroupLabel, SidebarMenuButton } from '@/components/ui/sidebar';
import { cn } from '@/lib/utils';

type Props = {
  children: ReactNode;
};

export const SettingsSidebarGroup: FC<Props> = ({ children }) => {
  return <SidebarGroup className="py-0">{children}</SidebarGroup>;
};

export const SettingsSidebarGroupLabel: FC<Props> = ({ children }) => {
  return <SidebarGroupLabel className="font-bold text-zinc-800 text-xs">{children}</SidebarGroupLabel>;
};

export const SettingsSidebarMenuButton: FC<Props & { isActive?: boolean }> = ({ children, isActive }) => {
  return (
    <SidebarMenuButton
      className={cn('py-5 hover:bg-zinc-400/35 transition-all duration-150', isActive && 'bg-zinc-400/20')}
    >
      {children}
    </SidebarMenuButton>
  );
};
