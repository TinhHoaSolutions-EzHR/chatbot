'use client';

import React, { useState } from 'react';

import { AdminHeader } from '@/components/admin-header';
import { ADMIN_ITEM_DETAIL } from '@/constants/admin-sidebar-items';
import { Route } from '@/constants/misc';

import { ConnectorsList } from './connectors-list/connectors-list';
import { SearchConnector } from './search-connector';

export default function ExistingConnectorsPage() {
  const [searchValue, setSearchValue] = useState<string>('');

  return (
    <>
      <AdminHeader adminItem={ADMIN_ITEM_DETAIL[Route.EXISTING_CONNECTORS]} />
      <SearchConnector setSearchValue={setSearchValue} />
      <ConnectorsList searchValue={searchValue} />
    </>
  );
}
