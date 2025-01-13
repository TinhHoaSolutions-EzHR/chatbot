'use client';

import { Search } from 'lucide-react';
import { FC } from 'react';

import { Input } from '@/components/ui/input';
import { LODASH_DEBOUNCE_TIME_MILLISECONDS } from '@/configs/misc';
import useCustomLodashDebounce from '@/hooks/utils/use-custom-lodash-debounce';

interface ISearchConnectorProps {
  setSearchValue(search: string): void;
}

export const SearchConnector: FC<ISearchConnectorProps> = ({ setSearchValue }) => {
  const debounceSetSearchValue = useCustomLodashDebounce((value: string) => {
    setSearchValue(value);
  }, LODASH_DEBOUNCE_TIME_MILLISECONDS);

  return (
    <div className="relative w-80">
      <Input
        className="pl-8"
        placeholder="Search existing connector..."
        onChange={e => {
          debounceSetSearchValue(e.target.value);
        }}
      />
      <Search className="absolute top-1/2 -translate-y-1/2 left-3" size={14} />
    </div>
  );
};
