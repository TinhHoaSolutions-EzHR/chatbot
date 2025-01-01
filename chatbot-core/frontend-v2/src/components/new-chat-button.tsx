'use client';

import { SquarePen } from 'lucide-react';
import { FC } from 'react';

import { Button } from './ui/button';
import { cn } from '@/lib/utils';

interface INewChatButtonProps {
  className?: string;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

export const NewChatButton: FC<INewChatButtonProps> = ({ className, onClick }) => {
  return (
    <Button
      variant="ghost"
      size="icon"
      className={cn('h-9 w-9', className)}
      onClick={event => {
        onClick?.(event);
      }}
    >
      <SquarePen className="size-5 text-muted-foreground" />
    </Button>
  );
};
