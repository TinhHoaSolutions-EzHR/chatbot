import { ChevronDown } from 'lucide-react';

import { Button } from './ui/button';

// TODO: Replace this with the actual logo
export const AppLogo = () => {
  return (
    <Button variant="ghost" className="p-2 flex gap-1 items-center">
      <p className="text-slate-600 text-lg font-semibold">EzHR</p>
      <ChevronDown className="size-3" />
    </Button>
  );
};
