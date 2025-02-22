import { MoreHorizontal } from 'lucide-react';
import { FC } from 'react';

import { DropdownMenu, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { SidebarMenuAction } from '@/components/ui/sidebar';
import { cn } from '@/lib/utils';
import { IChatSession } from '@/types/chat';

import { useChatSessionContext } from '../chat-session-context';
import { ActionsDropdown } from './actions-dropdown';
import { EditChatSessionButtons } from './edit-chat-session-buttons';

interface IChatSessionActionsProps {
  subItem?: boolean;
  chatSession: IChatSession;
  isOpenDropdown: boolean;
  setIsOpenDropdown(isOpen: boolean): void;
  setIsDropdownHovered(isHovered: boolean): void;
}

export const ChatSessionActions: FC<IChatSessionActionsProps> = ({
  subItem,
  chatSession,
  isOpenDropdown,
  setIsOpenDropdown,
  setIsDropdownHovered,
}) => {
  const { isEditingChatSession } = useChatSessionContext();

  return (
    <>
      {isEditingChatSession ? (
        <EditChatSessionButtons />
      ) : (
        <div className={cn('group-hover/chat-action:opacity-100 opacity-0', isOpenDropdown && 'opacity-100')}>
          <DropdownMenu open={isOpenDropdown} onOpenChange={setIsOpenDropdown}>
            <DropdownMenuTrigger asChild className={cn('bg-sidebar z-0', subItem && 'right-4')}>
              <SidebarMenuAction
                onMouseEnter={() => setIsDropdownHovered(true)}
                onMouseLeave={() => setIsDropdownHovered(false)}
              >
                <MoreHorizontal />
              </SidebarMenuAction>
            </DropdownMenuTrigger>
            <ActionsDropdown chatSession={chatSession} />
          </DropdownMenu>
        </div>
      )}
    </>
  );
};
