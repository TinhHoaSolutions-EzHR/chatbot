import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

import { StoreName } from '@/constants/misc';

interface IIndexStoreProps {
  connectors: {
    [connectorId: string]: string[];
  };
  addConnector(connectorId: string, taskId: string): void;
}

export const useIndexStore = create(
  persist<IIndexStoreProps>(
    set => ({
      connectors: {},
      addConnector(connectorId, taskId) {
        set(state => ({
          connectors: {
            ...state.connectors,
            [connectorId]: [...(state.connectors[connectorId] ?? []), taskId],
          },
        }));
      },
    }),
    {
      name: StoreName.INDEX_STORE,
      storage: createJSONStorage(() => localStorage),
    },
  ),
);
