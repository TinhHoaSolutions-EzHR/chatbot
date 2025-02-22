'use client';

import { Loader2 } from 'lucide-react';

import { TempChatModelIcon } from '@/components/temp-chat-model-icon';
import { Separator } from '@/components/ui/separator';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';

import { AgentPrompts } from './agent-prompts';
import { RecentAgents } from './recent-agents';

export default function NewChatPage() {
  const selectedAgent = useGetSelectedAgent();

  if (!selectedAgent) {
    return <Loader2 size={28} className="animate-spin text-muted-foreground" />;
  }

  return (
    <div className="chat-width">
      <div className="w-full flex justify-center">
        <h1 className="text-2xl font-semibold relative">
          {selectedAgent.name}
          <div className="absolute -left-16 top-1/2 -translate-y-1/2 p-3 rounded-full border border-dashed border-zinc-400">
            <TempChatModelIcon size={28} />
          </div>
        </h1>
      </div>
      <p className="text-center mt-6">{selectedAgent.description}</p>
      <div className="mt-6 w-full">
        <AgentPrompts agentId={selectedAgent.id} />
      </div>
      <Separator className="my-12" />
      <RecentAgents />
    </div>
  );
}
