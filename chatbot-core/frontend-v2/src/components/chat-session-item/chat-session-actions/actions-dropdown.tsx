'use client';

import { Hand, Pencil, Share, Trash2 } from 'lucide-react';
import { FC } from 'react';
import { toast } from 'sonner';

import { DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu';
import { useGetAllChatFolders } from '@/hooks/chat/use-get-all-chat-folders';
import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';
import { IChatSession } from '@/types/chat';

import { useChatSessionContext } from '../chat-session-context';

interface IActionsDropdownProps {
  chatSession: IChatSession;
}

export const ActionsDropdown: FC<IActionsDropdownProps> = ({ chatSession }) => {
  const { data: chatFolders } = useGetAllChatFolders();
  const { setIsEditingChatSession } = useChatSessionContext();
  const { openDialog } = useDialogStore();

  return (
    <DropdownMenuContent side="right" align="start">
      <DropdownMenuItem>
        <Share size={14} />
        Share
      </DropdownMenuItem>
      <DropdownMenuItem onClick={() => setIsEditingChatSession(true)}>
        <Pencil size={14} />
        Rename
      </DropdownMenuItem>
      <DropdownMenuItem
        onClick={() => {
          if (!chatFolders || !chatFolders.length) {
            toast.error('Something went wrong', {
              description: 'Please try again later.',
            });
            return;
          }

          openDialog(DialogType.MOVE_CHAT_SESSION, { chatSession });
        }}
      >
        <Hand size={14} />
        Move
      </DropdownMenuItem>
      <DropdownMenuItem onClick={() => openDialog(DialogType.DELETE_CHAT_SESSION, { chatSession })}>
        <Trash2 size={14} />
        Delete
      </DropdownMenuItem>
    </DropdownMenuContent>
  );
};
