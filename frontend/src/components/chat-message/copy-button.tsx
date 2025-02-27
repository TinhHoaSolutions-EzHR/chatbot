import { Check, Copy } from 'lucide-react';
import { FC, useState } from 'react';
import { toast } from 'sonner';

import { cn } from '@/lib/utils';

import WillRender from '../will-render';

const COPY_CHANGE_ICON_TIMEOUT = 1500;

interface ICopyButtonProps {
  content: string;
  className: string;
}

const CopyButton: FC<ICopyButtonProps> = ({ content, className }) => {
  const [isCopied, setIsCopied] = useState(false);

  const onCopy = async () => {
    if (isCopied) {
      return;
    }

    await navigator.clipboard.writeText(content);
    setIsCopied(true);
    toast.success('Successfully write to clipboard.', {
      duration: COPY_CHANGE_ICON_TIMEOUT,
    });
    setTimeout(() => {
      setIsCopied(false);
    }, COPY_CHANGE_ICON_TIMEOUT);
  };

  return (
    <div
      onClick={onCopy}
      className={cn('border p-2 rounded-sm cursor-pointer bg-white hidden group-hover:block', className)}
    >
      <WillRender when={isCopied}>
        <Check size={16} className="text-zinc-500" />
      </WillRender>
      <WillRender when={!isCopied}>
        <Copy size={16} className="text-zinc-500" />
      </WillRender>
    </div>
  );
};

export default CopyButton;
