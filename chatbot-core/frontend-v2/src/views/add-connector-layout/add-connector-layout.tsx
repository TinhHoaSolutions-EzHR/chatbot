import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import React, { ReactNode } from 'react';

import { Route } from '@/constants/misc';

type Props = {
  children: ReactNode;
};

export default function AddConnectorLayout({ children }: Props) {
  return (
    <div className="w-full flex justify-center">
      <div className="max-w-screen-md w-full">
        <Link
          href={Route.ADD_CONNECTOR}
          className="flex gap-1 items-center text-sm text-zinc-600 hover:underline underline-offset-4 cursor-pointer mb-8"
        >
          <ArrowLeft size={14} />
          Back to Add connector menu
        </Link>
        {children}
      </div>
    </div>
  );
}
