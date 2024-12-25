'use client';

import { AdminSidebar } from '@/components/admin/connectors/AdminSidebar';
import {
  ConnectorIconSkeleton,
  CpuIconSkeleton,
  NotebookIconSkeleton,
  SearchIcon,
  UsersIconSkeleton,
} from '@/components/icons/icons';
import { User, UserRole } from '@/lib/types';
import { UserDropdown } from '../UserDropdown';
import { usePathname } from 'next/navigation';
import { SettingsContext } from '../settings/SettingsProvider';
import { useContext } from 'react';

export function ClientLayout({ user, children }: { user: User | null; children: React.ReactNode }) {
  const isCurator = user?.role === UserRole.CURATOR || user?.role === UserRole.GLOBAL_CURATOR;
  const pathname = usePathname();
  const settings = useContext(SettingsContext);

  if (pathname.startsWith('/admin/connectors') || pathname.startsWith('/admin/embeddings')) {
    return <>{children}</>;
  }

  return (
    <div className="h-screen overflow-y-hidden">
      <div className="flex h-full">
        <div className="flex-none text-text-settings-sidebar bg-background-sidebar w-[250px] z-20 pt-4 pb-8 h-full border-r border-border miniscroll overflow-auto">
          <AdminSidebar
            collections={[
              {
                name: 'Connectors',
                items: [
                  {
                    name: (
                      <div className="flex">
                        <NotebookIconSkeleton className="text-icon-settings-sidebar" size={18} />
                        <div className="ml-1">Existing Connectors</div>
                      </div>
                    ),
                    link: '/admin/indexing/status',
                  },
                  {
                    name: (
                      <div className="flex">
                        <ConnectorIconSkeleton className="text-icon-settings-sidebar" size={18} />
                        <div className="ml-1.5">Add Connector</div>
                      </div>
                    ),
                    link: '/admin/add-connector',
                  },
                ],
              },
              ...(!isCurator
                ? [
                    {
                      name: 'Configuration',
                      items: [
                        {
                          name: (
                            <div className="flex">
                              <CpuIconSkeleton className="text-icon-settings-sidebar" size={18} />
                              <div className="ml-1">LLM</div>
                            </div>
                          ),
                          link: '/admin/configuration/llm',
                        },
                        {
                          error: settings?.settings.needs_reindexing,
                          name: (
                            <div className="flex">
                              <SearchIcon className="text-icon-settings-sidebar" />
                              <div className="ml-1">Search Settings</div>
                            </div>
                          ),
                          link: '/admin/configuration/search',
                        },
                      ],
                    },
                    {
                      name: 'User Management',
                      items: [
                        {
                          name: (
                            <div className="flex">
                              <UsersIconSkeleton className="text-icon-settings-sidebar" size={18} />
                              <div className="ml-1">Users</div>
                            </div>
                          ),
                          link: '/admin/users',
                        },
                      ],
                    },
                  ]
                : []),
            ]}
          />
        </div>
        <div className="pb-8 relative h-full overflow-y-auto w-full">
          <div className="fixed bg-background left-0 gap-x-4 mb-8 px-4 py-2 w-full items-center flex justify-end">
            <UserDropdown />
          </div>
          <div className="pt-20 flex overflow-y-auto overflow-x-hidden h-full px-4 md:px-12">{children}</div>
        </div>
      </div>
    </div>
  );
}
