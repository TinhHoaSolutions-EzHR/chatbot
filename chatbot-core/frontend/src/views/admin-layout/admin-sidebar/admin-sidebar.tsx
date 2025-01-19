'use client';

import { Undo } from 'lucide-react';
import Link from 'next/link';
import { FC } from 'react';

import AppLogo from '@/components/app-logo';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarSeparator,
} from '@/components/ui/sidebar';
import { Route } from '@/constants/misc';

import { AdminSidebarNavigations } from './admin-sidebar-navigations';
import { SettingsSidebarGroup, SettingsSidebarMenuButton } from './custom-sidebar-components';

export const AdminSidebar: FC = () => {
  return (
    <Sidebar>
      <SidebarHeader className="items-center">
        <Link href={Route.HOME_PAGE}>
          <AppLogo className="w-36 pb-4" />
        </Link>
      </SidebarHeader>
      <SidebarContent className="pb-2">
        <SettingsSidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <Link href={Route.HOME_PAGE}>
                <SidebarMenuItem>
                  <SettingsSidebarMenuButton>
                    <Undo size={14} />
                    Exit admin
                  </SettingsSidebarMenuButton>
                </SidebarMenuItem>
              </Link>
            </SidebarMenu>
          </SidebarGroupContent>
        </SettingsSidebarGroup>
        <SidebarSeparator />
        <AdminSidebarNavigations />
      </SidebarContent>
      <SidebarFooter className="border-t border-solid border-border">
        <div className="flex justify-center">
          <div className="flex gap-2 items-center">
            <div className="relative flex h-4 w-4 justify-center items-center">
              <span className="animate-ping absolute inline-flex h-4 w-4 rounded-full bg-green-300 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-green-400"></span>
            </div>
            <p className="text-sm leading-[30px] font-medium">EzHR - v0.1 alpha</p>
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
};
