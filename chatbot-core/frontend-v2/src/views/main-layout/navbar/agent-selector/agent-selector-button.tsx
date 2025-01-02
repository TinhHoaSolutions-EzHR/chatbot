import { ChevronDown } from 'lucide-react';
import { FC } from 'react';

import { TempChatModelIcon } from '@/components/temp-chat-model-icon';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';
import { cn } from '@/lib/utils';

interface IAgentSelectorButtonProps {
  isAgentSelectorOpen: boolean;
}

export const AgentSelectorButton: FC<IAgentSelectorButtonProps> = ({ isAgentSelectorOpen }) => {
  const selectedAgent = useGetSelectedAgent();

  if (!selectedAgent) {
    return <Skeleton className="rounded-3xl px-6 py-3 w-36 h-8" />;
  }

  return (
    <Button className="rounded-3xl shadow-md hover:shadow-lg transition-all duration-150 px-6 py-3">
      <TempChatModelIcon />
      <p className="font-bold">{selectedAgent.name}</p>
      <ChevronDown
        size={12}
        className={cn('text-sm transition-all duration-150 ease-linear ml-2', isAgentSelectorOpen && 'rotate-180')}
      />
    </Button>
  );
};
