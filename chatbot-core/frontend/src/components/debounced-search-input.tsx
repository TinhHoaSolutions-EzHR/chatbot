'use client';

import { Search } from 'lucide-react';
import { FC } from 'react';

import { Input } from '@/components/ui/input';
import { LODASH_DEBOUNCE_TIME_MILLISECONDS } from '@/configs/misc';
import useCustomLodashDebounce from '@/hooks/utils/use-custom-lodash-debounce';
import { cn } from '@/lib/utils';

interface IDebouncedSearchInputProps {
  setSearchValue(search: string): void;
  placeholder: string;
  className?: string;
}

export const DebouncedSearchInput: FC<IDebouncedSearchInputProps> = ({ setSearchValue, placeholder, className }) => {
  const debounceSetSearchValue = useCustomLodashDebounce((value: string) => {
    setSearchValue(value);
  }, LODASH_DEBOUNCE_TIME_MILLISECONDS);

  return (
    <div className={cn('relative w-80', className)}>
      <Input
        className="pl-8"
        placeholder={placeholder}
        onChange={e => {
          debounceSetSearchValue(e.target.value);
        }}
      />
      <Search className="absolute top-1/2 -translate-y-1/2 left-3" size={14} />
    </div>
  );
};
