import { FC, useState } from 'react';
import { toast } from 'sonner';

import { SidebarMenuItem, SidebarMenuSubItem } from '@/components/ui/sidebar';
import { useEditChatSession } from '@/hooks/chat/use-edit-chat-session';
import { cn } from '@/lib/utils';
import { IChatSession } from '@/types/chat';

import { ChatSessionActions } from './chat-session-actions';
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

  const { chatSessionDescription } = useChatSessionContext();

  const { mutate, isPending } = useEditChatSession();

  const onEditChatSession = () => {
    mutate(
      {
        chatSessionId: chatSession.id,
        data: {
          description: chatSessionDescription,
        },
      },
      {
        onSuccess() {
          toast.success('Modify chat description successfully.');
        },
        onError() {
          toast.error('Failed to modify chat description.', {
            description: "There's something wrong with your request. Please try again later!",
          });
        },
      },
    );
  };

  const SidebarItem = subItem ? SidebarMenuSubItem : SidebarMenuItem;

  return (
    <SidebarItem className={cn('group/chat-action cursor-pointer relative')}>
      <ChatSessionButton subItem={subItem} isDropdownHovered={isDropdownHovered} isOpenDropdown={isOpenDropdown}>
        <ChatSessionInput chatSession={chatSession} onEditChatSession={onEditChatSession} isPending={isPending} />
      </ChatSessionButton>
      <ChatSessionActions
        subItem
        chatSession={chatSession}
        isOpenDropdown={isOpenDropdown}
        setIsOpenDropdown={setIsOpenDropdown}
        setIsDropdownHovered={setIsDropdownHovered}
        isPending={isPending}
        onEditChatSession={onEditChatSession}
      />
    </SidebarItem>
  );
};

export default function ChatSessionItem(props: IChatSessionItemProps) {
  return (
    <ChatSessionProvider>
      <ChatSessionItemComponent {...props} />
    </ChatSessionProvider>
  );
}
