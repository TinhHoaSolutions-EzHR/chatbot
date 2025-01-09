'use client';

import { FC } from 'react';

import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
} from '@/components/ui/sidebar';
import { Skeleton } from '@/components/ui/skeleton';
import { useGetAllChatFolders } from '@/hooks/chat/use-get-all-chat-folders';

import { ChatFolderItem } from './chat-folder-item';

export const ChatFolders: FC = () => {
  const { data: chatFolders, isLoading } = useGetAllChatFolders();

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
              <ChatFolderItem key={folder.id} folder={folder} isDefaultOpen={idx === 0} />
            ))
          )}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  );
};
