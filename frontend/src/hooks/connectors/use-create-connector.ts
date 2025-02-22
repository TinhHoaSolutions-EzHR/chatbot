import { useMutation } from '@tanstack/react-query';

import { ReactMutationKey } from '@/constants/react-query-key';
import { createConnector } from '@/services/connectors/create-connector';

export const useCreateConnector = () => {
  return useMutation({
    mutationKey: [ReactMutationKey.CREATE_CONNECTOR],
    mutationFn: createConnector,
  });
};
