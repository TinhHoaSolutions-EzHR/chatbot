import { ReactNode } from 'react';

import MainLayoutView from '@/views/main-layout/main-layout';

type Props = {
  children: ReactNode;
};

export default function MainLayout({ children }: Props) {
  return <MainLayoutView>{children}</MainLayoutView>;
}
