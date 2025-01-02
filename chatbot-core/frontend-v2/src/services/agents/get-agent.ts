import { MOCK_AGENT_PROMPTS, MOCK_AGENTS_LIST } from '@/configs/mock-agents';
import { IAgentWithPrompts } from '@/types/agent';

export const getAgent: (agentId: string) => Promise<IAgentWithPrompts | null> = async agentId => {
  return new Promise<IAgentWithPrompts | null>(resolve => {
    const agent = MOCK_AGENTS_LIST.find(agent => agent.id === agentId);
    const agentWithPrompt = agent ? { ...agent, prompts: MOCK_AGENT_PROMPTS[agent.id] } : null;

    resolve(agentWithPrompt);
  });
};
