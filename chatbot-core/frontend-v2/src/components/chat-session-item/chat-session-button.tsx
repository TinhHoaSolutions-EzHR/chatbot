import { FC, ReactNode } from 'react';

import { cn } from '@/lib/utils';

import { SidebarMenuButton, SidebarMenuSubButton } from '../ui/sidebar';

interface IChatSessionButtonProps {
  subItem?: boolean;
  isOpenDropdown: boolean;
  isDropdownHovered: boolean;
  children: ReactNode;
}

export const ChatSessionButton: FC<IChatSessionButtonProps> = ({
  subItem,
  isOpenDropdown,
  isDropdownHovered,
  children,
}) => {
  const SidebarButton = subItem ? SidebarMenuSubButton : SidebarMenuButton;

  return (
    <SidebarButton asChild>
      <div
        className={cn(
          'relative whitespace-nowrap group/chat-item',
          (isOpenDropdown || isDropdownHovered) && 'bg-sidebar-accent',
        )}
      >
        {children}
        <div
          className={cn(
            'absolute top-0 bottom-0 -right-4 w-10 bg-more-gradient z-0 group-hover/chat-item:bg-more-gradient-hover group-hover/chat-item:w-20',
            (isOpenDropdown || isDropdownHovered) && 'bg-more-gradient-hover w-20',
          )}
        />
      </div>
    </SidebarButton>
  );
};
