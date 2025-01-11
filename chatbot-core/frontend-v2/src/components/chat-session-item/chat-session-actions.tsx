import { Check, MoreHorizontal, Pencil, Share, Trash2, X } from 'lucide-react';
import { FC } from 'react';
import { toast } from 'sonner';

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useDeleteChatSession } from '@/hooks/chat/use-delete-chat-session';
import { useConfirm } from '@/hooks/utils/use-confirm';
import { cn } from '@/lib/utils';
import { IChatSession } from '@/types/chat';

import { SidebarMenuAction } from '../ui/sidebar';
import { useChatSessionContext } from './chat-session-context';

interface IChatSessionActionsProps {
  subItem?: boolean;
  chatSession: IChatSession;
  isOpenDropdown: boolean;
  setIsOpenDropdown(isOpen: boolean): void;
  setIsDropdownHovered(isHovered: boolean): void;
  isPending: boolean;
  onEditChatSession(): void;
}

export const ChatSessionActions: FC<IChatSessionActionsProps> = ({
  subItem,
  chatSession,
  isOpenDropdown,
  setIsOpenDropdown,
  setIsDropdownHovered,
  isPending,
  onEditChatSession,
}) => {
  const { isEditingChatSession, setIsEditingChatSession } = useChatSessionContext();
  const [ConfirmDialog, confirm] = useConfirm('Are you sure', 'You are about to delete this chat session.');

  const { mutate } = useDeleteChatSession(chatSession.id);

  const onDeleteChatSession = async () => {
    const ok = await confirm();

    if (!ok) {
      return;
    }

    mutate(chatSession.id, {
      onSuccess() {
        toast.success('Delete chat successfully.');
      },
      onError() {
        toast.error('Delete chat failed.', {
          description: "There's something wrong with your request. Please try again later!",
        });
      },
    });
  };

  return (
    <>
      <ConfirmDialog />
      {isEditingChatSession ? (
        <div className={cn('absolute top-0 bottom-0 right-2 gap-2 items-center group-hover/folder:flex flex')}>
          <Check size={14} className="text-muted-foreground hover:text-zinc-800" onClick={onEditChatSession} />
          <X
            size={14}
            className="text-muted-foreground hover:text-zinc-800"
            onClick={() => !isPending && setIsEditingChatSession(false)}
          />
        </div>
      ) : (
        <div className={cn('group-hover/chat-action:opacity-100 opacity-0', isOpenDropdown && 'opacity-100')}>
          <DropdownMenu open={isOpenDropdown} onOpenChange={setIsOpenDropdown}>
            <DropdownMenuTrigger asChild className={cn('bg-sidebar z-0', subItem && 'right-4')}>
              <SidebarMenuAction
                onMouseEnter={() => setIsDropdownHovered(true)}
                onMouseLeave={() => setIsDropdownHovered(false)}
              >
                <MoreHorizontal />
              </SidebarMenuAction>
            </DropdownMenuTrigger>
            <DropdownMenuContent side="right" align="start">
              <DropdownMenuItem>
                <Share size={14} />
                Share
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setIsEditingChatSession(true)}>
                <Pencil size={14} />
                Rename
              </DropdownMenuItem>
              <DropdownMenuItem onClick={onDeleteChatSession}>
                <Trash2 size={14} />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      )}
    </>
  );
};
