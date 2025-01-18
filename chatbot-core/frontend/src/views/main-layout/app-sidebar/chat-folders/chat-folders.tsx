'use client';

import { FC, useMemo } from 'react';

import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
} from '@/components/ui/sidebar';
import { Skeleton } from '@/components/ui/skeleton';
import { useGetAllChatFolders } from '@/hooks/chat/use-get-all-chat-folders';
import { useGetAllChatSessions } from '@/hooks/chat/use-get-all-chat-sessions';
import { IChatSession } from '@/types/chat';

import { ChatFolderItem } from './chat-folder-item';

export const ChatFolders: FC = () => {
  const { data: chatFolders, isLoading } = useGetAllChatFolders();
  const { data: chatSessions } = useGetAllChatSessions();

  const mappedFolderToChatSessions = useMemo(() => {
    if (!chatSessions) {
      return {};
    }

    return chatSessions.reduce<Record<string, IChatSession[]>>((acc, cur) => {
      if (!cur.folder_id) {
        return acc;
      }

      if (!acc[cur.folder_id]) {
        acc[cur.folder_id] = [];
      }

      acc[cur.folder_id].push(cur);

      return acc;
    }, {});
  }, [chatSessions]);

  return (
    <SidebarGroup>
      <SidebarGroupLabel className="font-bold text-zinc-600">Chat folders</SidebarGroupLabel>
      <SidebarGroupContent>
        <SidebarMenu>
          {isLoading || !chatFolders ? (
            <Skeleton className="w-full h-12 rounded" />
          ) : chatFolders.length === 0 ? (
            <SidebarMenuItem>No folder created yet.</SidebarMenuItem>
          ) : (
            chatFolders.map((folder, idx) => (
              <ChatFolderItem
                key={folder.id}
                folder={folder}
                chatSessions={mappedFolderToChatSessions[folder.id]}
                isDefaultOpen={idx === 0}
              />
            ))
          )}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  );
};
