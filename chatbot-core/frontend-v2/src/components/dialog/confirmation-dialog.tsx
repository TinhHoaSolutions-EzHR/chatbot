import { FC, ReactNode } from 'react';

import { Button } from '../ui/button';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '../ui/dialog';

interface IConfirmationDialogProps {
  children?: ReactNode;
  title: string;
  description: string;
  isOpen: boolean;
  onConfirm?(): void;
  onClose(): void;
  customConfirmContent?: string;
  customCloseContent?: string;
  preventClose?: boolean;
  customFooter?: boolean;
}

export const ConfirmationDialog: FC<IConfirmationDialogProps> = ({
  children,
  title,
  description,
  isOpen,
  onConfirm,
  onClose,
  customConfirmContent,
  customCloseContent,
  preventClose,
  customFooter,
}) => {
  return (
    <Dialog open={isOpen || preventClose} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        {children}
        {!customFooter && (
          <DialogFooter className="mt-6">
            <Button disabled={preventClose} onClick={onConfirm}>
              {customConfirmContent ?? 'Confirm'}
            </Button>
            <Button disabled={preventClose} onClick={onClose} variant="outline">
              {customCloseContent ?? 'Cancel'}
            </Button>
          </DialogFooter>
        )}
      </DialogContent>
    </Dialog>
  );
};
