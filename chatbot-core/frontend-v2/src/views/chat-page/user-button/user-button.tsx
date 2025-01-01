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
        <UserDropdownItem icon="Settings" onClick={() => {}}>
          Admin panel
        </UserDropdownItem>
        <UserDropdownItem icon="User" onClick={() => {}}>
          User settings
        </UserDropdownItem>
        <UserDropdownItem icon="Bell" onClick={() => {}}>
          Notifications
        </UserDropdownItem>
        <DropdownMenuSeparator />
        <UserDropdownItem icon="LogOut" onClick={() => {}}>
          Logout
        </UserDropdownItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
