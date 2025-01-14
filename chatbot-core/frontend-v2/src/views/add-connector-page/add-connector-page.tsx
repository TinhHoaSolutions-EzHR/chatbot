'use client';

import { useRouter } from 'next/navigation';
import { FC, useMemo, useState } from 'react';

import { DebouncedSearchInput } from '@/components/debounced-search-input';
import { Route } from '@/constants/misc';
import withRenderAdminHeader from '@/hoc/with-render-admin-header';
import { searchConnectorOptions } from '@/utils/search-connector-options';

const AddConnectorPage: FC = () => {
  const router = useRouter();
  const [searchValue, setSearchValue] = useState<string>('');

  const filteredConnectorProviders = useMemo(() => searchConnectorOptions(searchValue), [searchValue]);

  return (
    <>
      <DebouncedSearchInput setSearchValue={setSearchValue} placeholder="Search connector provider..." />
      <div className="mt-8 space-y-8">
        {filteredConnectorProviders.map(({ title, description, connectors }) => (
          <div key={title}>
            <h3 className="text-xl font-medium text-zinc-900">{title}</h3>
            <p className="text-sm text-zinc-500">{description}</p>
            <div className="flex gap-4 mt-4">
              {connectors.map(({ href, name, icon }) => (
                <div
                  key={href}
                  onClick={() => router.push(href)}
                  className="flex flex-col items-center justify-center p-4 rounded-lg w-40 cursor-pointer shadow-md hover:bg-zinc-100 bg-zinc-50 transition-all duration-150"
                >
                  {icon}
                  <p className="text-sm font-medium mt-2">{name}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </>
  );
};

export default withRenderAdminHeader(AddConnectorPage, Route.ADD_CONNECTOR);
