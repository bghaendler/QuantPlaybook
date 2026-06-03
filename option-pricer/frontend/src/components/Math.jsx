import React, { useEffect, useRef } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

export const InlineMath = ({ math }) => {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current) {
      try {
        katex.render(math, ref.current, {
          displayMode: false,
          throwOnError: false,
          trust: true
        });
      } catch (err) {
        ref.current.textContent = math;
      }
    }
  }, [math]);
  return <span ref={ref} />;
};

export const BlockMath = ({ math }) => {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current) {
      try {
        katex.render(math, ref.current, {
          displayMode: true,
          throwOnError: false,
          trust: true
        });
      } catch (err) {
        ref.current.textContent = math;
      }
    }
  }, [math]);
  return <div ref={ref} style={{ overflowX: 'auto', overflowY: 'hidden' }} />;
};
