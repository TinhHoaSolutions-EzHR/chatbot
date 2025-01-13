import React, { FC } from 'react';

import { IAdminItemDetail } from '@/constants/admin-sidebar-items';

import { Separator } from './ui/separator';

interface IAdminHeaderProps {
  adminItem: IAdminItemDetail;
}

export const AdminHeader: FC<IAdminHeaderProps> = ({ adminItem }) => {
  const Icon = adminItem.icon;

  return (
    <>
      <div className="flex gap-2 items-center">
        <Icon size={30} />
        <h1 className="text-3xl font-bold">{adminItem.name}</h1>
      </div>
      <Separator className="my-4" />
    </>
  );
};
