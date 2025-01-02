import { FC, ReactNode } from 'react';

import { TempChatModelIcon } from '@/components/temp-chat-model-icon';
import { useGetAgentsList } from '@/hooks/agents/use-get-agents-list';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';
import { useAgentStore } from '@/hooks/stores/use-agent-store';
import { cn } from '@/lib/utils';
import { IAgent } from '@/types/agent';

interface IOptionProps {
  agent: IAgent;
  avatar: ReactNode;
  isSelected: boolean;
}

const Option: FC<IOptionProps> = ({ agent, avatar, isSelected }) => {
  const { setSelectedAgent } = useAgentStore();

  return (
    <div
      className={cn(
        'px-3 py-4 rounded-xl cursor-pointer hover:bg-zinc-200/30 flex items-center gap-4',
        isSelected && 'bg-zinc-300/40 hover:bg-zinc-300/40',
      )}
      onClick={() => setSelectedAgent(agent)}
    >
      {avatar}
      <div className="overflow-hidden text-ellipsis break-words flex-grow">
        <h3 className="line-clamp-1 text-sm font-semibold leading-tight">{agent.name}</h3>
        <p className="line-clamp-2 text-xs text-muted-foreground">{agent.description}</p>
      </div>
    </div>
  );
};

export const AgentSelectorOptions = () => {
  const { data: agentsList } = useGetAgentsList();
  const { searchContent } = useAgentStore();
  const selectedAgent = useGetSelectedAgent();

  const filteredAgents = agentsList?.filter(agent => agent.name.toLowerCase().includes(searchContent.toLowerCase()));

  return (
    <div className="space-y-2">
      {filteredAgents?.map(agent => (
        <Option
          key={agent.id}
          agent={agent}
          avatar={<TempChatModelIcon />}
          isSelected={selectedAgent?.id === agent.id}
        />
      ))}
    </div>
  );
};
