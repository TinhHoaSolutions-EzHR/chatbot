import React, { FC } from 'react';

import { IConnector } from '@/types/connector';

interface IConnectorItemProps {
  connector: IConnector;
}

export const ConnectorItem: FC<IConnectorItemProps> = () => {
  return <div>ConnectorItem</div>;
};
