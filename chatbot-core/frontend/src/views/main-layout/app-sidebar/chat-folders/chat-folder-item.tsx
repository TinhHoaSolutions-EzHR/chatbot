import { useDroppable } from '@dnd-kit/core';
import { FC, useState } from 'react';

import ChatSessionItem from '@/components/chat-session-item/chat-session-item';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { SidebarMenuItem, SidebarMenuSub } from '@/components/ui/sidebar';
import { cn } from '@/lib/utils';
import { IChatSession, IFolder } from '@/types/chat';

import { ChatFolderActions } from './chat-folder-actions/chat-folder-actions';

interface IChatFolderItemProps {
  folder: IFolder;
  chatSessions: IChatSession[] | undefined;
  isDefaultOpen?: boolean;
}

export const ChatFolderItem: FC<IChatFolderItemProps> = ({ folder, chatSessions, isDefaultOpen }) => {
  const [isFolderOpen, setIsFolderOpen] = useState<boolean>(!!isDefaultOpen);
  const { isOver, setNodeRef } = useDroppable({
    id: folder.id,
  });
  const style = {
    backgroundColor: isOver ? 'rgba(0, 0, 0, 0.1)' : undefined,
  };

  return (
    <Collapsible
      ref={setNodeRef}
      style={style}
      defaultOpen={isDefaultOpen}
      className={cn('group/collapsible')}
      open={isFolderOpen}
      onOpenChange={setIsFolderOpen}
    >
      <SidebarMenuItem>
        <CollapsibleTrigger asChild>
          <div>
            <ChatFolderActions folder={folder} isFolderOpen={isFolderOpen} />
          </div>
        </CollapsibleTrigger>
        <CollapsibleContent>
          {chatSessions && chatSessions.length > 0 && (
            <SidebarMenuSub>
              {chatSessions.map(session => (
                <ChatSessionItem key={session.id} chatSession={session} subItem />
              ))}
            </SidebarMenuSub>
          )}
        </CollapsibleContent>
      </SidebarMenuItem>
    </Collapsible>
  );
};
