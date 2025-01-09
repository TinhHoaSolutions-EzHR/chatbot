import { FC, useState } from 'react';

import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { SidebarMenuItem, SidebarMenuSub, SidebarMenuSubButton, SidebarMenuSubItem } from '@/components/ui/sidebar';
import { IChatSession, IFolder } from '@/types/chat';

import { ChatFolderActions } from './chat-folder-actions/chat-folder-actions';

interface IChatFolderItemProps {
  folder: IFolder;
  chatSessions: IChatSession[] | undefined;
  isDefaultOpen?: boolean;
}

export const ChatFolderItem: FC<IChatFolderItemProps> = ({ folder, chatSessions, isDefaultOpen }) => {
  const [isFolderOpen, setIsFolderOpen] = useState<boolean>(!!isDefaultOpen);

  return (
    <Collapsible
      defaultOpen={isDefaultOpen}
      className="group/collapsible"
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
              <SidebarMenuSubItem>
                {chatSessions.map(session => (
                  <SidebarMenuSubButton key={session.id} className="cursor-pointer">
                    {session.description ?? session.id}
                  </SidebarMenuSubButton>
                ))}
              </SidebarMenuSubItem>
            </SidebarMenuSub>
          )}
        </CollapsibleContent>
      </SidebarMenuItem>
    </Collapsible>
  );
};
