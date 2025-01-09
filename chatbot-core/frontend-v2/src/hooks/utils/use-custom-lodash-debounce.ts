import debounce from 'lodash/debounce';
import { useEffect, useMemo, useRef } from 'react';

// NOTE: This component is a work-around for avoiding re-render input when using debounce
// ref: https://www.developerway.com/posts/debouncing-in-react

const useCustomLodashDebounce = (callback: (...params: any[]) => void, waitTime: number) => {
  const ref = useRef<(...params: any[]) => void>();

  useEffect(() => {
    ref.current = callback;
  }, [callback]);

  return useMemo(() => {
    const func = (...params: any[]) => {
      ref.current?.(...params);
    };

    return debounce(func, waitTime);
  }, [waitTime]);
};

export default useCustomLodashDebounce;
