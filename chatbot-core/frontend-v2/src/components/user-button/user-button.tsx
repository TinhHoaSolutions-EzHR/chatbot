import { Bell, LogOut, Settings, User } from 'lucide-react';

import { Avatar, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useGetUserInfo } from '@/hooks/user/use-get-user-info';
import { useUserLogout } from '@/hooks/user/use-user-logout';

import { UserDropdownItem } from './user-dropdown-item';

export const UserButton = () => {
  const { data: userInfo } = useGetUserInfo();
  const logout = useUserLogout();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Avatar className="cursor-pointer">
          <AvatarImage src={userInfo?.avatar} />
        </Avatar>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <UserDropdownItem Icon={Settings} onClick={() => {}}>
          Admin panel
        </UserDropdownItem>
        <UserDropdownItem Icon={User} onClick={() => {}}>
          User settings
        </UserDropdownItem>
        <UserDropdownItem Icon={Bell} onClick={() => {}}>
          Notifications
        </UserDropdownItem>
        <DropdownMenuSeparator />
        <UserDropdownItem Icon={LogOut} onClick={logout}>
          Logout
        </UserDropdownItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
