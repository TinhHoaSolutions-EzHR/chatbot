'use client';

import { LucideIcon } from 'lucide-react';
import { FC, ReactNode } from 'react';

import { DropdownMenuItem } from '@/components/ui/dropdown-menu';

interface IUserDropdownItemProps {
  Icon: LucideIcon;
  children: ReactNode;
  onClick(): void;
}

export const UserDropdownItem: FC<IUserDropdownItemProps> = ({ Icon, children, onClick }) => {
  return (
    <DropdownMenuItem className="flex gap-2 items-center cursor-pointer pl-4 py-3 pr-12" onClick={onClick}>
      <Icon className="size-3.5 text-slate-600" />
      <p className="font-medium text-slate-600">{children}</p>
    </DropdownMenuItem>
  );
};
