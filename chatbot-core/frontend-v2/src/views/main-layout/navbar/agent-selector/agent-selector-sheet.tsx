import { Separator } from '@/components/ui/separator';
import { SheetContent, SheetTitle } from '@/components/ui/sheet';

import { AgentSelectorOptions } from './agent-selector-options';
import { AgentSelectorSearchBar } from './agent-selector-search-bar';

export const AgentSelectorSheet = () => {
  return (
    <SheetContent side="bottom">
      <SheetTitle className="text-center">Choose your agent</SheetTitle>
      <AgentSelectorSearchBar className="mt-6" />
      <Separator className="my-3 bg-zinc-300" />
      <AgentSelectorOptions />
    </SheetContent>
  );
};
