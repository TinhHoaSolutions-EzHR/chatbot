'use client';

import React from 'react';

import { cn } from '@/lib/utils';

import styles from './auto-height-textarea.module.css';

interface IAutoHeightTextareaProps extends React.ComponentProps<'textarea'> {
  wrapperClassName?: string;
}

const AutoHeightTextarea = React.forwardRef<HTMLTextAreaElement, IAutoHeightTextareaProps>(
  ({ className, wrapperClassName, onChange, ...props }, ref) => {
    const [value, setValue] = React.useState('');

    const onTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      onChange?.(e);
      setValue(e.target.value);
    };

    return (
      <div className={cn(styles.GrowWrap, wrapperClassName)} data-replicated-value={value}>
        {/* Hard coded rows value, this is to ensure that the min height of the text area is
        only one row, the css will handle the auto resizing for us. */}
        <textarea rows={1} className={className} ref={ref} onChange={onTextareaChange} {...props}></textarea>
      </div>
    );
  },
);
AutoHeightTextarea.displayName = 'AutoHeightTextarea';

export { AutoHeightTextarea };
