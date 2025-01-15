import { ReactNode } from 'react';

import AddConnectorLayout from '@/views/add-connector-layout/add-connector-layout';

type Props = {
  children: ReactNode;
};

export default function Layout({ children }: Props) {
  return <AddConnectorLayout>{children}</AddConnectorLayout>;
}
