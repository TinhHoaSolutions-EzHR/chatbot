import { ArrowLeft, Check, Cog, X } from 'lucide-react';
import { useRouter } from 'next/navigation';
import React, { FC } from 'react';

import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import WillRender from '@/components/will-render';
import { Route } from '@/constants/misc';
import { cn } from '@/lib/utils';

interface IAddFileConnectorProgress {
  isError: boolean;
  progressLabel: string;
  progress: number;
}

export const AddFileConnectorProgress: FC<IAddFileConnectorProgress> = ({ isError, progress, progressLabel }) => {
  const router = useRouter();

  return (
    <WillRender when={progress !== 0}>
      <div className="w-full mt-12 flex flex-col gap-2 justify-center items-center">
        <div className="flex gap-1 items-center">
          <WillRender>
            <WillRender.If when={isError}>
              <X className="text-rose-600" />
            </WillRender.If>
            <WillRender.If when={progress !== 100}>
              <Cog className="animate-spin duration-1000 ease-in-out" />
            </WillRender.If>
            <WillRender.Else>
              <Check className="text-emerald-600" />
            </WillRender.Else>
          </WillRender>
          <p className={cn('font-bold', isError && 'text-rose-600')}>{progressLabel}</p>
        </div>
        <Progress className="w-[60%] h-4" value={progress} />
        <WillRender when={progress === 100}>
          <Button onClick={() => router.push(Route.EXISTING_CONNECTORS)} className="mt-2 gap-1" variant="ghost">
            <ArrowLeft size={14} /> Back to Connectors
          </Button>
        </WillRender>
      </div>
    </WillRender>
  );
};
