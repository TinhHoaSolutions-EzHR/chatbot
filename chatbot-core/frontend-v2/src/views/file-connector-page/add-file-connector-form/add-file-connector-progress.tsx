import { Check, Cog, X } from 'lucide-react';
import React, { FC } from 'react';

import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';

interface IAddFileConnectorProgress {
  isError: boolean;
  progressLabel: string;
  progress: number;
}

export const AddFileConnectorProgress: FC<IAddFileConnectorProgress> = ({ isError, progress, progressLabel }) => {
  if (progress === 0) {
    return null;
  }

  return (
    <div className="w-full mt-12 flex flex-col gap-2 justify-center items-center">
      <div className="flex gap-1 items-center">
        {isError ? (
          <X className="text-rose-600" />
        ) : progress !== 100 ? (
          <Cog className="animate-spin duration-1000 ease-in-out" />
        ) : (
          <Check className="text-emerald-600" />
        )}
        <p className={cn('font-bold', isError && 'text-rose-600')}>{progressLabel}</p>
      </div>
      <Progress className="w-[60%] h-4" value={progress} />
    </div>
  );
};
