'use client';

import React, { FC, useState } from 'react';

import { DebouncedSearchInput } from '@/components/debounced-search-input';
import { Route } from '@/constants/misc';
import withRenderAdminHeader from '@/hoc/with-render-admin-header';

import { ConnectorsList } from './connectors-list/connectors-list';

const ExistingConnectorsPage: FC = () => {
  const [searchValue, setSearchValue] = useState<string>('');

  return (
    <>
      <DebouncedSearchInput setSearchValue={setSearchValue} placeholder="Search existing connectors..." />
      <ConnectorsList searchValue={searchValue} />
    </>
  );
};

export default withRenderAdminHeader(ExistingConnectorsPage, Route.EXISTING_CONNECTORS);
