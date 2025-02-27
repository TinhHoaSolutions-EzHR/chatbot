import React, { FC, ReactNode } from 'react';

interface WillRenderProps {
  when?: boolean;
  children?: ReactNode;
}

const WillRender: FC<WillRenderProps> & {
  If: FC<WillRenderProps>;
  Else: FC<{ children?: ReactNode }>;
} = ({ when, children }) => {
  if (when !== undefined) {
    return when ? <>{children}</> : null;
  }

  const shouldRender = true;
  const validChildren = React.Children.toArray(children).filter(child => React.isValidElement<WillRenderProps>(child));

  for (const child of validChildren) {
    if (!React.isValidElement(child) || (child.type !== If && child.type !== Else)) {
      throw new Error('Will render if and else must be used inside of WillRender');
    }

    if ('when' in child.props) {
      if (child.props.when && shouldRender) {
        return child;
      }
    } else {
      return child;
    }
  }

  return null;
};

const If: FC<WillRenderProps> = ({ when, children }) => (when ? <>{children}</> : null);
const Else: FC<Pick<WillRenderProps, 'children'>> = ({ children }) => <>{children}</>;

WillRender.If = If;
WillRender.Else = Else;

export default WillRender;
