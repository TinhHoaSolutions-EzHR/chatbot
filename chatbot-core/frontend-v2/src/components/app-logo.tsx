import React from 'react';

type Props = React.PropsWithChildren<React.ComponentPropsWithRef<'button'>>;

const AppLogo = (props: Props) => {
  return (
    <button {...props}>
      <img src="/TinhHoaSolutionsImage.png" className="w-full h-full" />
    </button>
  );
};

export default AppLogo;
