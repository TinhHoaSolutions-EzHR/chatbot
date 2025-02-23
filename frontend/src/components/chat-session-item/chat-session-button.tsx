import { useDraggable } from '@dnd-kit/core';
import { FC, ReactNode } from 'react';

import { cn } from '@/lib/utils';

import { SidebarMenuButton, SidebarMenuSubButton } from '../ui/sidebar';

interface IChatSessionButtonProps {
  id: string;
  subItem?: boolean;
  isOpenDropdown: boolean;
  isDropdownHovered: boolean;
  children: ReactNode;

  onClick?(): void;
}

export const ChatSessionButton: FC<IChatSessionButtonProps> = ({
  id,
  subItem,
  isOpenDropdown,
  isDropdownHovered,
  children,
  onClick,
}) => {
  const SidebarButton = subItem ? SidebarMenuSubButton : SidebarMenuButton;
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: id,
  });
  const style = transform
    ? {
        transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
      }
    : undefined;
  return (
    <SidebarButton asChild onClick={onClick}>
      <div
        ref={setNodeRef}
        style={style}
        {...listeners}
        {...attributes}
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
