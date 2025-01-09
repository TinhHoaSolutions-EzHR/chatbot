import { MoreHorizontal, Pencil, Share, Trash2 } from 'lucide-react';
import { FC, useState } from 'react';

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { SidebarMenuAction, SidebarMenuButton, SidebarMenuItem } from '@/components/ui/sidebar';
import { cn } from '@/lib/utils';
import { IChatSession } from '@/types/chat';

interface IChatSessionItemProps {
  chatSession: IChatSession;
}

export const ChatSessionItem: FC<IChatSessionItemProps> = ({ chatSession }) => {
  const [isOpenDropdown, setIsOpenDropdown] = useState<boolean>(false);
  const [isDropdownHovered, setIsDropdownHovered] = useState<boolean>(false);

  return (
    <SidebarMenuItem className="group/chat-action">
      <SidebarMenuButton asChild>
        <div
          className={cn(
            'relative whitespace-nowrap group/chat-item',
            (isOpenDropdown || isDropdownHovered) && 'bg-sidebar-accent',
          )}
        >
          {chatSession.description ?? chatSession.id}
          <div
            className={cn(
              'absolute top-0 bottom-0 right-0 w-10 bg-more-gradient z-0 group-hover/chat-item:bg-more-gradient-hover group-hover/chat-item:w-20',
              (isOpenDropdown || isDropdownHovered) && 'bg-more-gradient-hover w-20',
            )}
          />
        </div>
      </SidebarMenuButton>
      <div className={cn('group-hover/chat-action:opacity-100 opacity-0', isOpenDropdown && 'opacity-100')}>
        <DropdownMenu open={isOpenDropdown} onOpenChange={setIsOpenDropdown}>
          <DropdownMenuTrigger asChild className="bg-sidebar">
            <SidebarMenuAction
              onMouseEnter={() => setIsDropdownHovered(true)}
              onMouseLeave={() => setIsDropdownHovered(false)}
            >
              <MoreHorizontal />
            </SidebarMenuAction>
          </DropdownMenuTrigger>
          <DropdownMenuContent side="right" align="start">
            <DropdownMenuItem>
              <Share size={14} />
              Share
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Pencil size={14} />
              Rename
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Trash2 size={14} />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </SidebarMenuItem>
  );
};
