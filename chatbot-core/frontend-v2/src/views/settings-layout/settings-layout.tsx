import { ReactNode } from 'react';

import { SidebarProvider } from '@/components/ui/sidebar';

type Props = {
  children: ReactNode;
};

export default function SettingsLayoutView({ children }: Props) {
  return (
    <SidebarProvider open={true}>
      <div>{children}</div>
    </SidebarProvider>
  );
}
