import { File, TriangleAlert } from 'lucide-react';
import React, { FC } from 'react';

import { IConnector } from '@/types/connector';

import { ConnectorItem } from './connector-item';

interface IConnectorsTableProps {
  connectors: IConnector[];
}

const ConnectorsTable: FC<IConnectorsTableProps> = ({ connectors }) => {
  return (
    <div className="border-l border-r border-b border-solid">
      <div className="grid-connectors-table border-t border-solid bg-slate-200/20 py-8 px-4">
        <div className="flex text-xl font-semibold items-center gap-2">
          <File size={20} className="text-blue-500" /> File
        </div>
        <div className="text-sm text-slate-600 font-medium">
          Total connectors<p className="font-semibold text-xl">{connectors.length}</p>
        </div>
        <div className="text-sm text-slate-600 font-medium">
          Active connectors
          <p className="font-semibold text-xl">
            {connectors.length}/{connectors.length}
          </p>
        </div>
        <div className="text-sm text-slate-600 font-medium">
          Total docs indexed
          <p className="font-semibold text-xl">
            {connectors.reduce((acc, cur) => acc + (cur.connector_specific_config?.file_paths.length ?? 0), 0)}
          </p>
        </div>
        <div className="text-sm text-slate-600 font-medium">
          Errors
          <p className="flex gap-1 items-center font-semibold text-xl">
            <TriangleAlert size={20} className="text-rose-500" /> 0
          </p>
        </div>
      </div>
      <div className="grid-connectors-table border-t border-solid px-4 py-4">
        <p className="text-sm text-slate-500 font-medium col-span-2">Name</p>
        <p className="text-sm text-slate-500 font-medium">Activity</p>
        <p className="text-sm text-slate-500 font-medium">Total docs</p>
        <p className="text-sm text-slate-500 font-medium">Last status</p>
      </div>
      {connectors.map(connector => (
        <ConnectorItem key={connector.id} connector={connector} />
      ))}
    </div>
  );
};

export default ConnectorsTable;
