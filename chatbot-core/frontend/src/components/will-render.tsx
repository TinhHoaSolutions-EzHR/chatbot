import { ReactNode, useEffect, useState } from 'react';

import { cn } from '@/lib/utils';

interface IWillRenderProps {
  children: ReactNode;
  isActive: boolean;
  onActive?: () => void;
  shouldHideOnInactive?: boolean;
}

export default function WillRender({ children, isActive, onActive, shouldHideOnInactive }: IWillRenderProps) {
  const [isComponentMounted, setIsComponentMounted] = useState(false);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    if (isActive && !isComponentMounted) {
      setIsComponentMounted(true);
    }

    onActive?.();
  }, [isActive]);

  // Check if the component is mounted on the client
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Prevent rendering until the component is mounted on the client
  if (!isClient) {
    return null;
  }

  // Prevent rendering if the component is not active and not mounted (initial render)
  if (!isActive && !isComponentMounted) {
    return null;
  }

  return <div className={cn(!isActive && shouldHideOnInactive && 'opacity-0')}>{children}</div>;
}
