'use client';

import { Loader2 } from 'lucide-react';

import { useGetAgent } from '@/hooks/agents/use-get-agent';
import { useGetSelectedAgent } from '@/hooks/agents/use-get-selected-agent';

export const NewChat = () => {
  const selectedAgent = useGetSelectedAgent();
  const { data: agentWithPrompts, isPending } = useGetAgent(selectedAgent?.id);

  if (!selectedAgent) {
    return <Loader2 size={28} className="animate-spin text-muted-foreground" />;
  }

  return <>Hello world</>;
};
