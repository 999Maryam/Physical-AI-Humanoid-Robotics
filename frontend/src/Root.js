import React from 'react';
import FloatingChatbot from './components/FloatingChatbot';

function Root({ children }) {
  return (
    <>
      {children}
      <FloatingChatbot />
    </>
  );
}

export default Root;