import { MOCK_RECENT_AGENTS } from '@/configs/mock-agents';
import { IAgent } from '@/types/agent';

export const getRecentAgents: () => Promise<IAgent[]> = async () => {
  return new Promise<IAgent[]>(resolve => {
    resolve(MOCK_RECENT_AGENTS);
  });
};
