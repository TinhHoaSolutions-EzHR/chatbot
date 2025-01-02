import { FC } from 'react';

interface ITempChatModelIconProps {
  className?: string;
}

export const TempChatModelIcon: FC<ITempChatModelIconProps> = ({ className }) => {
  return (
    <svg className={className} width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="4" height="4" fill="#6FB1FF"></rect>
      <rect x="8" y="0" width="4" height="4" fill="#6FB1FF"></rect>
      <rect x="4" y="4" width="4" height="4" fill="#6FB1FF"></rect>
      <rect x="8" y="4" width="4" height="4" fill="#6FB1FF"></rect>
      <rect x="12" y="4" width="4" height="4" fill="#6FB1FF"></rect>
      <rect x="0" y="8" width="4" height="4" fill="#6FB1FF"></rect>
      <rect x="12" y="8" width="4" height="4" fill="#6FB1FF"></rect>
      <rect x="0" y="12" width="4" height="4" fill="#6FB1FF"></rect>
      <rect x="8" y="12" width="4" height="4" fill="#6FB1FF"></rect>
    </svg>
  );
};
