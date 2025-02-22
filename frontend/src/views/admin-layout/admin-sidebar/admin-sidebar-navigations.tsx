import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FC } from 'react';

import { SidebarGroupContent, SidebarMenu, SidebarMenuItem } from '@/components/ui/sidebar';
import { ADMIN_SIDEBAR_ITEMS } from '@/constants/admin-sidebar-items';

import {
  SettingsSidebarGroup,
  SettingsSidebarGroupLabel,
  SettingsSidebarMenuButton,
} from './custom-sidebar-components';

export const AdminSidebarNavigations: FC = () => {
  const pathname = usePathname();

  return (
    <>
      {ADMIN_SIDEBAR_ITEMS.map(({ label, items }, idx) => (
        <SettingsSidebarGroup key={idx}>
          <SettingsSidebarGroupLabel>{label}</SettingsSidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map(({ name, href, icon }, idx) => {
                const Icon = icon;
                const isActive = pathname.includes(href);

                return (
                  <Link key={idx} href={href}>
                    <SidebarMenuItem>
                      <SettingsSidebarMenuButton isActive={isActive}>
                        <Icon size={14} /> {name}
                      </SettingsSidebarMenuButton>
                    </SidebarMenuItem>
                  </Link>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SettingsSidebarGroup>
      ))}
    </>
  );
};
