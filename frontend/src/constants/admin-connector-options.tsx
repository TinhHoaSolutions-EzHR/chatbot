import { File, Globe } from 'lucide-react';
import { ReactNode } from 'react';

import { Route } from './misc';

interface IAdminConnectorProps {
  name: string;
  icon: ReactNode;
  href: Route;
}

export interface IAdminConnectorOption {
  title: string;
  description: string;
  connectors: IAdminConnectorProps[];
}

export const ADMIN_CONNECTOR_OPTIONS: IAdminConnectorOption[] = [
  {
    title: 'Storage',
    description: 'Connect to cloud storage and file hosting services.',
    connectors: [
      {
        name: 'File',
        icon: <File size={24} className="text-blue-600" />,
        href: Route.ADD_FILE_CONNECTOR,
      },
      {
        name: 'Google drive',
        icon: <img src="/GoogleDrive.png" className="size-6" />,
        href: Route.ADD_GOOGLE_DRIVE_CONNECTOR,
      },
    ],
  },
  {
    title: 'Other',
    description: 'Connect to other miscellaneous knowledge sources.',
    connectors: [
      {
        name: 'Web',
        icon: <Globe size={24} className="text-blue-600" />,
        href: Route.ADD_WEB_CONNECTOR,
      },
    ],
  },
];
