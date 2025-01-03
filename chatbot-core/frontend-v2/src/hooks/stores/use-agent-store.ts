import { create } from 'zustand';

import { IAgent } from '@/types/agent';

interface IAgentStore {
  searchContent: string;
  selectedAgent: IAgent | null;

  setSearchContent: (content: string) => void;
  setSelectedAgent: (agent: IAgent) => void;
}

export const useAgentStore = create<IAgentStore>(set => ({
  searchContent: '',
  selectedAgent: null,

  setSearchContent(content) {
    set({ searchContent: content });
  },
  setSelectedAgent(agent) {
    set({ selectedAgent: agent });
  },
}));
