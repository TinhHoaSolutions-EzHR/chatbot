import { Trash2 } from 'lucide-react';
import { FC } from 'react';
import { toast } from 'sonner';

import { useDeleteChatFolder } from '@/hooks/chat/use-delete-chat-folder';
import { useConfirm } from '@/hooks/utils/use-confirm';
import { IFolder } from '@/types/chat';

interface IDeleteChatFolderButtonProps {
  folder: IFolder;
}

export const DeleteChatFolderButton: FC<IDeleteChatFolderButtonProps> = ({ folder }) => {
  const [ConfirmDialog, confirm] = useConfirm(
    'Are you sure?',
    'You are about to delete this folder along with its Chats.',
  );

  const { mutate } = useDeleteChatFolder(folder.id);

  const onDeleteChatFolder = async () => {
    const ok = await confirm();

    if (ok) {
      mutate(folder.id, {
        onSuccess() {
          toast.success('Folder deleted successfully');
        },
        onError() {
          toast.error('Folder did not deleted', {
            description: "There's something wrong with your request, please try again later.",
          });
        },
      });
    }
  };

  return (
    <>
      <ConfirmDialog />
      <Trash2 size={14} className="text-muted-foreground hover:text-zinc-800" onClick={onDeleteChatFolder} />
    </>
  );
};
