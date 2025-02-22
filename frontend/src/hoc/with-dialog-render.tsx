import React, { ComponentType, useEffect, useState } from 'react';

import { DialogType, useDialogStore } from '@/hooks/stores/use-dialog-store';

/**
 * Higher-order component (HOC) to conditionally render a wrapped component
 * after it is active, that is, if it is not mounted, will return `null`, if yes,
 * then keep its state.
 *
 * @template P - The props type of the wrapped component.
 * @param {ComponentType<P>} Dialog - The component to be wrapped.
 * @param {DialogType} dialogType - The specific dialog type to match against the dialog store.
 * @returns {ComponentType<P>} - The enhanced component that renders conditionally.
 *
 * @description
 * This HOC:
 * - Subscribes to the dialog store to monitor the current dialog type.
 * - Renders the `Dialog` only when the `dialogType` matches the current dialog type from the store.
 * - Ensures the `Dialog` is mounted only once, even after the dialog is closed.
 * - Prevent client actions (hooks, functions, etc.) to be run when the `Dialog` is not mounted.
 *
 * @example
 * ```tsx
 * import React from 'react';
 * import withDialogRender from './withDialogRender';
 * import { DialogType } from '@/hooks/stores/use-dialog-store';
 *
 * const MyDialogComponent: React.FC = () => {
 *   return <div>This is a dialog component.</div>;
 * };
 *
 * export default withDialogRender(MyDialogComponent, DialogType.MyDialog);
 * ```
 */
const withDialogRender = <P extends object>(Dialog: ComponentType<P>, dialogType: DialogType) => {
  const HOC = (props: P) => {
    const [isComponentMounted, setIsComponentMounted] = useState(false);
    const [isClient, setIsClient] = useState(false);

    const currentDialogType = useDialogStore(state => state.dialogType);
    const isOpenDialog = currentDialogType === dialogType;

    useEffect(() => {
      if (isOpenDialog && !isComponentMounted) {
        setIsComponentMounted(true);
      }
    }, [isOpenDialog]);

    useEffect(() => {
      setIsClient(true);
    }, []);

    if (!isClient) {
      return null;
    }

    if (!isOpenDialog && !isComponentMounted) {
      return null;
    }

    return <Dialog {...(props as P)} />;
  };

  // Set the display name for the HOC
  HOC.displayName = `${Dialog.displayName || Dialog.name || 'Component'}`;

  return HOC;
};

export default withDialogRender;
