import React, { ComponentType } from 'react';

import { Separator } from '@/components/ui/separator';
import { ADMIN_ITEM_DETAIL } from '@/constants/admin-sidebar-items';
import { Route } from '@/constants/misc';

/**
 * Higher-order component (HOC) to render an admin page with a standardized header.
 *
 * @template P - The props type of the wrapped admin page component.
 * @param {ComponentType<P>} AdminPage - The admin page component to be wrapped.
 * @param {Route} route - The route key used to retrieve admin item details for the header.
 * @returns {ComponentType<P>} - The enhanced component with the admin header.
 *
 * @description
 * This HOC:
 * - Retrieves admin item details (e.g., icon, name) based on the `route` parameter.
 * - Prepends a header containing an icon, name, and a separator to the wrapped admin page.
 * - Allows consistent styling and structure for admin page headers.
 */
const withRenderAdminHeader = <P extends object>(AdminPage: ComponentType<P>, route: Route) => {
  const HOC = (props: P) => {
    const adminItem = ADMIN_ITEM_DETAIL[route];

    const Icon = adminItem.icon;

    return (
      <>
        <div className="flex gap-2 items-center">
          <Icon size={30} />
          <h1 className="text-3xl font-bold">{adminItem.name}</h1>
        </div>
        <Separator className="my-4" />
        <AdminPage {...(props as P)} />
      </>
    );
  };

  // Set the display name for the HOC
  HOC.displayName = `${AdminPage.displayName || AdminPage.name || 'Component'}`;

  return HOC;
};

export default withRenderAdminHeader;
