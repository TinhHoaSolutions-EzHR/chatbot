import { useState } from 'react';

import { SidebarMenuItem, SidebarMenuSubItem } from '@/components/ui/sidebar';
import { cn } from '@/lib/utils';
import { IChatSession } from '@/types/chat';

import { ChatSessionActions } from './chat-session-actions/chat-session-actions';
import { ChatSessionButton } from './chat-session-button';
import { ChatSessionProvider } from './chat-session-context';
import { ChatSessionInput } from './chat-session-input';

interface IChatSessionItemProps {
  chatSession: IChatSession;
  subItem?: boolean;
}

export default function ChatSessionItemComponent({ chatSession, subItem }: IChatSessionItemProps) {
  const [isOpenDropdown, setIsOpenDropdown] = useState<boolean>(false);
  const [isDropdownHovered, setIsDropdownHovered] = useState<boolean>(false);

  const SidebarItem = subItem ? SidebarMenuSubItem : SidebarMenuItem;

  return (
    <ChatSessionProvider chatSession={chatSession}>
      <SidebarItem className={cn('group/chat-action cursor-pointer relative')}>
        <ChatSessionButton subItem={subItem} isDropdownHovered={isDropdownHovered} isOpenDropdown={isOpenDropdown}>
          <ChatSessionInput chatSession={chatSession} />
        </ChatSessionButton>
        <ChatSessionActions
          subItem
          chatSession={chatSession}
          isOpenDropdown={isOpenDropdown}
          setIsOpenDropdown={setIsOpenDropdown}
          setIsDropdownHovered={setIsDropdownHovered}
        />
      </SidebarItem>
    </ChatSessionProvider>
  );
}
