import { FC, ReactNode, useMemo } from 'react';
import { toast } from 'sonner';

import { TempChatModelIcon } from '@/components/temp-chat-model-icon';
import { useGetAgentsList } from '@/hooks/agents/use-get-agents-list';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';
import { useSelectAgent } from '@/hooks/agents/use-select-agent';
import { useAgentStore } from '@/hooks/stores/use-agent-store';
import { cn } from '@/lib/utils';
import { IAgent } from '@/types/agent';

interface IOptionProps {
  agent: IAgent;
  avatar: ReactNode;
  isSelected: boolean;
}

const Option: FC<IOptionProps> = ({ agent, avatar, isSelected }) => {
  const { mutate } = useSelectAgent();
  const { setSelectedAgent } = useAgentStore();

  return (
    <div
      className={cn(
        'px-3 py-4 rounded-xl cursor-pointer hover:bg-zinc-200/30 flex items-center gap-4',
        isSelected && 'bg-zinc-300/40 hover:bg-zinc-300/40',
      )}
      onClick={() => {
        setSelectedAgent(agent);
        mutate(agent.id, {
          onError() {
            toast.error('Select agent error', {
              description: "There's something wrong with your request, please try again later",
            });
            setSelectedAgent(null);
          },
        });
      }}
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
  const { agentsList } = useGetAgentsList().data ?? {};
  const { searchContent } = useAgentStore();
  const selectedAgent = useGetSelectedAgent();

  const filteredAgents = useMemo(() => {
    if (!searchContent || !agentsList) {
      return agentsList;
    }

    return agentsList.filter(agent => agent.name.toLowerCase().includes(searchContent.toLowerCase()));
  }, [agentsList]);

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
