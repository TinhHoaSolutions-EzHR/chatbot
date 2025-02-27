'use client';

import { ArchiveX } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FC, useMemo } from 'react';

import WillRender from '@/components/will-render';
import { Route } from '@/constants/misc';
import { useGetAllConnectors } from '@/hooks/connectors/use-get-all-connectors';

import { ConnectorSkeleton } from './connector-skeleton';
import ConnectorsTable from './connectors-table';

interface IConnectorsListProps {
  searchValue: string;
}

export const ConnectorsList: FC<IConnectorsListProps> = ({ searchValue }) => {
  const { data: connectors, isLoading, isError } = useGetAllConnectors();
  const router = useRouter();

  const filteredConnectors = useMemo(() => {
    if (!connectors) {
      return undefined;
    }

    if (!searchValue) {
      return connectors;
    }

    const cleanedSearchValue = searchValue.trim().toLowerCase();

    return connectors.filter(
      connector => connector.name.toLowerCase() === cleanedSearchValue || connector.source === cleanedSearchValue,
    );
  }, [searchValue, connectors]);

  if (isError) {
    router.push(Route.ERROR_PAGE);
  }

  if (!filteredConnectors) {
    return <div className="mt-8 flex justify-center items-center w-full"></div>;
  }

  if (filteredConnectors.length === 0) {
    return (
      <div className="py-20 mt-6 gap-4 flex flex-col w-full items-center justify-center border rounded-lg bg-[#f9f9f9] shadow">
        <ArchiveX size={64} />
        <p className="text-sm text-muted-foreground">
          No connectors found.{' '}
          <Link href={Route.ADD_CONNECTOR} className="text-foreground font-semibold underline underline-offset-4">
            Create one
          </Link>
        </p>
      </div>
    );
  }

  return (
    <div className="mt-8 flex flex-col gap-4">
      <WillRender>
        <WillRender.If when={isLoading || !filteredConnectors}>
          {Array.from({ length: 3 }).map((_, idx) => (
            <ConnectorSkeleton key={idx} />
          ))}
        </WillRender.If>
        <WillRender.Else>
          <ConnectorsTable connectors={filteredConnectors} />
        </WillRender.Else>
      </WillRender>
    </div>
  );
};
