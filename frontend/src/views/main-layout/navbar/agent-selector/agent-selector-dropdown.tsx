import { DropdownMenuContent } from '@/components/ui/dropdown-menu';
import { Separator } from '@/components/ui/separator';

import { AgentSelectorOptions } from './agent-selector-options';
import { AgentSelectorSearchBar } from './agent-selector-search-bar';

export const AgentSelectorDropdown = () => {
  return (
    <DropdownMenuContent>
      <h1 className="text-lg text-center font-bold mt-4">Choose your agent</h1>
      <div className="min-w-96 p-4">
        <AgentSelectorSearchBar />
        <Separator className="my-3 bg-zinc-300" />
        <AgentSelectorOptions />
      </div>
    </DropdownMenuContent>
  );
};
