'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

import { Route } from '@/constants/misc';

export default function Page() {
  const router = useRouter();

  useEffect(() => {
    router.push(Route.EXISTING_CONNECTORS);
  }, []);

  return <></>;
}
