import { CreateChatFolderDialog } from '@/components/dialog/create-chat-folder-dialog/create-chat-folder-dialog';
import { DeleteChatFolderDialog } from '@/components/dialog/delete-chat-folder-dialog/delete-chat-folder-dialog';
import { DeleteChatSessionDialog } from '@/components/dialog/delete-chat-session-dialog/delete-chat-session-dialog';
import { MoveChatSessionDialog } from '@/components/dialog/move-chat-session-dialog/move-chat-session-dialog';

export default function DialogProvider() {
  return (
    <>
      <CreateChatFolderDialog />
      <DeleteChatFolderDialog />

      <MoveChatSessionDialog />
      <DeleteChatSessionDialog />
    </>
  );
}
