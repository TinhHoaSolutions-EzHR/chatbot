import { useRouter } from 'next/navigation';
import { FC, useState } from 'react';

import { SidebarMenuItem, SidebarMenuSubItem } from '@/components/ui/sidebar';
import { QueryParams, Route } from '@/constants/misc';
import { cn } from '@/lib/utils';
import { IChatSession } from '@/types/chat';

import { ChatSessionActions } from './chat-session-actions/chat-session-actions';
import { ChatSessionButton } from './chat-session-button';
import { ChatSessionProvider, useChatSessionContext } from './chat-session-context';
import { ChatSessionInput } from './chat-session-input';

interface IChatSessionItemProps {
  chatSession: IChatSession;
  subItem?: boolean;
}

const ChatSessionItemComponent: FC<IChatSessionItemProps> = ({ chatSession, subItem }) => {
  const [isOpenDropdown, setIsOpenDropdown] = useState<boolean>(false);
  const [isDropdownHovered, setIsDropdownHovered] = useState<boolean>(false);

  const { isEditingChatSession } = useChatSessionContext();

  const router = useRouter();

  const SidebarItem = subItem ? SidebarMenuSubItem : SidebarMenuItem;

  return (
    <SidebarItem className={cn('group/chat-action cursor-pointer relative')}>
      <ChatSessionButton
        id={chatSession.id}
        subItem={subItem}
        isDropdownHovered={isDropdownHovered}
        isOpenDropdown={isOpenDropdown}
        onClick={() => {
          if (!isEditingChatSession) {
            router.push(`${Route.CHAT}/?${QueryParams.CHAT_SESSION_ID}=${chatSession.id}`);
          }
        }}
      >
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
  );
};

export default function ChatSessionItem(props: IChatSessionItemProps) {
  return (
    <ChatSessionProvider chatSession={props.chatSession}>
      <ChatSessionItemComponent {...props} />
    </ChatSessionProvider>
  );
}
