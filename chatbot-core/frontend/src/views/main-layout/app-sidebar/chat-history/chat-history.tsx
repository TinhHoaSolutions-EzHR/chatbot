import { useDroppable } from '@dnd-kit/core';
import { FC, useMemo } from 'react';

import ChatSessionItem from '@/components/chat-session-item/chat-session-item';
import { SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarMenu } from '@/components/ui/sidebar';
import { useGetAllChatSessions } from '@/hooks/chat/use-get-all-chat-sessions';
import { groupChatSessions } from '@/utils/group-chat-sessions';

export const ChatHistory: FC = () => {
  const { data: chatSessions } = useGetAllChatSessions();

  const groupedChatSessions = useMemo(
    () => (chatSessions ? groupChatSessions(chatSessions.filter(session => !session.folder_id)) : undefined),
    [chatSessions],
  );
  const { isOver, setNodeRef } = useDroppable({
    id: 'chat-history',
  });
  const style = {
    color: isOver ? 'green' : undefined,
  };
  return (
    <>
      <div ref={setNodeRef} style={style}>
        <h3 className="text-xs font-bold text-zinc-600 ml-4 mt-2">History</h3>
        {groupedChatSessions?.map(group => (
          <SidebarGroup key={group.title}>
            <SidebarGroupLabel>{group.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {group.chatSessions.map(chatSession => (
                  <ChatSessionItem key={chatSession.id} chatSession={chatSession} />
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </div>
    </>
  );
};
