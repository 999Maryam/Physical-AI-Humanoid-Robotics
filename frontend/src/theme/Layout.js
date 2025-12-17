import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import FloatingChatbot from '../components/FloatingChatbot';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <FloatingChatbot />
    </>
  );
}