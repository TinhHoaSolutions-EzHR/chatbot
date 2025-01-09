import { ReactNode } from 'react';

import SettingsLayoutView from '@/views/settings-layout/settings-layout';

type Props = {
  children: ReactNode;
};

export default function MainLayout({ children }: Props) {
  return <SettingsLayoutView>{children}</SettingsLayoutView>;
}
