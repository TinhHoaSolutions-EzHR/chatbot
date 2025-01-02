import { Bell, LogOut, Settings, User } from 'lucide-react';

import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

import { UserDropdownItem } from './user-dropdown-item';

export const UserButton = () => {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Avatar className="cursor-pointer">
          <AvatarFallback>NN</AvatarFallback>
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
        <UserDropdownItem Icon={LogOut} onClick={() => {}}>
          Logout
        </UserDropdownItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
