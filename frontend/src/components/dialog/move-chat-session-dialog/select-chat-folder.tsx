import { FC } from 'react';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils';
import { IFolder } from '@/types/chat';

import { MOVE_TO_CHAT_HISTORY_VALUE } from './move-chat-session-dialog';

interface ISelectChatFolderProps {
  selectedFolder: string;
  setSelectedFolder(folder: string): void;
  chatFolders: IFolder[] | undefined;
  previousFolder: IFolder | null | undefined;
}

export const SelectChatFolder: FC<ISelectChatFolderProps> = ({
  selectedFolder,
  setSelectedFolder,
  chatFolders,
  previousFolder,
}) => {
  return (
    <Select value={selectedFolder} onValueChange={value => setSelectedFolder(value)}>
      <SelectTrigger className={cn(selectedFolder === MOVE_TO_CHAT_HISTORY_VALUE && '!text-rose-500')}>
        <SelectValue placeholder="Select a folder" />
      </SelectTrigger>
      <SelectContent>
        {chatFolders?.map(folder => (
          <SelectItem key={folder.id} value={folder.id}>
            {folder.name ?? folder.id}
          </SelectItem>
        ))}
        {previousFolder && (
          <>
            <Separator className="my-2" />
            <SelectItem value={MOVE_TO_CHAT_HISTORY_VALUE} className="font-medium !text-rose-500">
              Remove from folder {previousFolder.name ?? previousFolder.id}
            </SelectItem>
          </>
        )}
      </SelectContent>
    </Select>
  );
};
