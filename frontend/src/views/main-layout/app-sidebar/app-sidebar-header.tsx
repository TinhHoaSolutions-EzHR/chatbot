'use client';

import { FolderPlus, Layers, LucideIcon } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { FC } from 'react';

import { NewChatButton } from '@/components/new-chat-button';
import { SidebarHeader, SidebarTrigger } from '@/components/ui/sidebar';
import { Route } from '@/constants/misc';
import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';

interface IActionButtonProps {
  icon: LucideIcon;
  children: string;
  onClick(): void;
}

const ActionButton: FC<IActionButtonProps> = ({ icon, children, onClick }) => {
  const ButtonIcon = icon;
  return (
    <div
      onClick={onClick}
      className="
        w-full p-2 bg-white border-zinc-300/70 border
        rounded items-center hover:bg-zinc-200/90 cursor-pointer
        transition-all duration-150 flex gap-x-2 text-black"
    >
      <ButtonIcon size={18} />
      <p className="text-sm">{children}</p>
    </div>
  );
};

export const AppSidebarHeader: FC = () => {
  const router = useRouter();
  const openDialog = useDialogStore(state => state.openDialog);

  return (
    <SidebarHeader>
      <div className="w-full flex justify-between">
        <SidebarTrigger />
        <NewChatButton onClick={() => router.push(Route.HOME_PAGE)} />
      </div>
      <div className="space-y-1 w-full">
        <ActionButton icon={FolderPlus} onClick={() => openDialog(DialogType.CREATE_CHAT_FOLDER)}>
          New folder
        </ActionButton>
        <ActionButton icon={Layers} onClick={() => router.push(Route.MANAGE_ASSISTANTS)}>
          Manage assistants
        </ActionButton>
      </div>
    </SidebarHeader>
  );
};
