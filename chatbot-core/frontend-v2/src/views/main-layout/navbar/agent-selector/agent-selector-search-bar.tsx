import { Search } from 'lucide-react';
import { FC, useState } from 'react';

import { Input } from '@/components/ui/input';
import { LODASH_DEBOUNCE_TIME_MILLISECONDS } from '@/configs/misc';
import { useAgentStore } from '@/hooks/stores/use-agent-store';
import useCustomLodashDebounce from '@/hooks/use-custom-lodash-debounce';
import { cn } from '@/lib/utils';

interface IAgentSelectorSearchBarProps {
  className?: string;
}

export const AgentSelectorSearchBar: FC<IAgentSelectorSearchBarProps> = ({ className }) => {
  const [searchValue, setSearchValue] = useState('');
  const { setSearchContent } = useAgentStore();

  const debounceSetSearchContent = useCustomLodashDebounce((value: string) => {
    setSearchContent(value);
  }, LODASH_DEBOUNCE_TIME_MILLISECONDS);

  const onSearchInputChange = (value: string) => {
    setSearchValue(value);
    debounceSetSearchContent(value);
  };

  return (
    <div className={cn('w-full relative', className)}>
      <Search size={16} className="absolute top-1/2 -translate-y-1/2 left-3 text-muted-foreground" />
      <Input
        className="w-full pl-9"
        value={searchValue}
        onChange={e => onSearchInputChange(e.target.value)}
        placeholder="Search for assistant..."
      />
    </div>
  );
};
