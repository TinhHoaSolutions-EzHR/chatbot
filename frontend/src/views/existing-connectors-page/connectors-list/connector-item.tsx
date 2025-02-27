import React, { FC } from 'react';

import { Badge } from '@/components/ui/badge';
import { useGetIndexStatus } from '@/hooks/documents/use-get-index-status';
import { useIndexStore } from '@/hooks/stores/use-index-store';
import { cn } from '@/lib/utils';
import { IConnector } from '@/types/connector';
import { IndexStatus } from '@/types/document';

function mapIndexStatus(status: IndexStatus | undefined) {
  const STATUS_MAP = {
    [IndexStatus.PENDING]: 'Queueing',
    [IndexStatus.STARTED]: 'Indexing',
    [IndexStatus.SUCCESS]: 'Success',
    [IndexStatus.FAILURE]: 'Failed',
  };

  const STATUS_CLASS_MAP = {
    [IndexStatus.PENDING]: 'bg-transparent hover:bg-transparent text-slate-400 border-slate-400',
    [IndexStatus.STARTED]: 'bg-transparent hover:bg-transparent text-yellow-600 border-yellow-600',
    [IndexStatus.SUCCESS]: 'bg-transparent hover:bg-transparent text-emerald-600 border-emerald-600',
    [IndexStatus.FAILURE]: 'bg-transparent hover:bg-transparent text-rose-600 border-rose-600',
  };

  return (
    <Badge className={cn('rounded-xl px-2', STATUS_CLASS_MAP[status ?? IndexStatus.PENDING])}>
      {STATUS_MAP[status ?? IndexStatus.PENDING]}
    </Badge>
  );
}

interface IConnectorItemProps {
  connector: IConnector;
}

export const ConnectorItem: FC<IConnectorItemProps> = ({ connector }) => {
  const taskIds = useIndexStore(state => state.connectors[connector.id]);
  const { data: indexStatus } = useGetIndexStatus(taskIds ? taskIds.at(-1) : undefined);

  return (
    <div className="grid-connectors-table border-t border-solid px-4 py-4">
      <p className="font-medium text-sm col-span-2">{connector.name}</p>
      <div>
        <Badge className="bg-emerald-500 hover:bg-emerald-400 rounded-xl">Active</Badge>
      </div>
      <p className="font-medium text-sm">{connector.connector_specific_config?.file_paths.length ?? 0}</p>
      <div>{mapIndexStatus(indexStatus?.status)}</div>
    </div>
  );
};
