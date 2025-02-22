'use client';

import { Loader2 } from 'lucide-react';
import { ReactNode } from 'react';

import { useApiHealthCheck } from '@/hooks/use-api-health-check';

type Props = {
  children: ReactNode;
};

export default function HealthCheckProvider({ children }: Props) {
  const { isLoading, isError } = useApiHealthCheck();

  if (isLoading) {
    return (
      <div className="full-screen-center">
        <Loader2 size={32} className="animate-spin" />
      </div>
    );
  }

  if (isError) {
    return <div className="full-screen-center">EzHR didn't set up properly</div>;
  }

  return <>{children}</>;
}
