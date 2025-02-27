'use client';

import { Hand, Pencil, Share, Trash2 } from 'lucide-react';
import { FC } from 'react';
import { toast } from 'sonner';

import { DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu';
import { DEFAULT_NEW_CHAT_NAME } from '@/constants/misc';
import { useGetAllChatFolders } from '@/hooks/chat/use-get-all-chat-folders';
import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';
import { IChatSession } from '@/types/chat';
import ToastService from '@/utils/default-toasts';

import { useChatSessionContext } from '../chat-session-context';

interface IActionsDropdownProps {
  chatSession: IChatSession;
}

export const ActionsDropdown: FC<IActionsDropdownProps> = ({ chatSession }) => {
  const { data: chatFolders } = useGetAllChatFolders();
  const { setIsEditingChatSession, setChatSessionDescription } = useChatSessionContext();
  const openDialog = useDialogStore(state => state.openDialog);

  return (
    <DropdownMenuContent side="right" align="start">
      <DropdownMenuItem>
        <Share size={14} />
        Share
      </DropdownMenuItem>
      <DropdownMenuItem
        onClick={() => {
          setIsEditingChatSession(true);
          setChatSessionDescription(chatSession.description ?? DEFAULT_NEW_CHAT_NAME);
        }}
      >
        <Pencil size={14} />
        Rename
      </DropdownMenuItem>
      <DropdownMenuItem
        onClick={() => {
          if (!chatFolders) {
            ToastService.apiFail();
            return;
          }

          if (chatFolders.length === 0) {
            toast.error("You don't have a folder yet", {
              description: 'Please create one before continue.',
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
