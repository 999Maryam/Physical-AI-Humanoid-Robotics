import React, { useState, useRef } from 'react';
import { sendChatQuery } from '../services/chatbot_api';
import styles from './Chatbot.module.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Tracks if bot is processing
  const [retryInfo, setRetryInfo] = useState(null); // Tracks retry status
  const lastRequestTime = useRef(0); // For throttling

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    // Throttle: prevent sending messages too quickly (min 500ms between requests)
    const now = Date.now();
    const timeSinceLastRequest = now - lastRequestTime.current;
    if (timeSinceLastRequest < 500 && lastRequestTime.current !== 0) {
      console.log('Throttled: Please wait before sending another message');
      return;
    }
    lastRequestTime.current = now;

    // Add user's message
    const userMessage = { id: Date.now(), text: input, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);

    // Show "Thinking..." message
    setIsLoading(true);
    setRetryInfo(null); // Clear any previous retry info
    const thinkingMessageId = Date.now() + 1;
    const thinkingMessage = {
      id: thinkingMessageId,
      text: 'Thinking...',
      sender: 'bot',
      isThinking: true,
    };
    setMessages((prev) => [...prev, thinkingMessage]);

    const queryText = input;
    setInput(''); // Clear input field immediately

    try {
      // Call API with retry callback for UI updates
      const data = await sendChatQuery(queryText, null, null, (attempt, maxRetries, backoffTime) => {
        // Update retry info for user feedback
        setRetryInfo({
          attempt,
          maxRetries,
          backoffTime: Math.round(backoffTime / 1000), // Convert to seconds
        });

        // Update thinking message to show retry status
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === thinkingMessageId
              ? {
                  ...msg,
                  text: `Rate limit reached. Retrying in ${Math.round(backoffTime / 1000)}s... (${attempt}/${maxRetries})`,
                }
              : msg
          )
        );
      });

      // Clear retry info on success
      setRetryInfo(null);

      // Replace "Thinking..." with actual bot response
      const botMessage = {
        id: Date.now() + 2,
        text: data.text,
        sender: 'bot',
        sourceReferences: data.source_references,
      };

      setMessages((prev) =>
        prev
          .filter((msg) => msg.id !== thinkingMessageId) // Remove thinking message
          .concat(botMessage)
      );
    } catch (error) {
      console.error('Error sending message:', error);

      // Clear retry info
      setRetryInfo(null);

      // Determine error message based on error type
      let errorMessage = 'Error: Could not get a response from the chatbot.';

      if (error.statusCode === 429 || error.message === 'RATE_LIMIT') {
        errorMessage = '⚠️ Rate limit exceeded. The service is busy right now. Please try again in a moment.';
      } else if (error.statusCode === 500) {
        errorMessage = '⚠️ Server error. The AI service is temporarily unavailable. Please try again later.';
      } else if (error.message && error.message.includes('Failed to fetch')) {
        errorMessage = '⚠️ Network error. Please check your connection and try again.';
      }

      // Replace thinking message with error
      setMessages((prev) =>
        prev
          .filter((msg) => msg.id !== thinkingMessageId)
          .concat({
            id: Date.now() + 2,
            text: errorMessage,
            sender: 'bot',
            isError: true,
          })
      );
    } finally {
      setIsLoading(false); // Stop loading state
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.messagesList}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`${styles.message} ${styles[msg.sender]} ${
              msg.isThinking ? styles.thinking : ''
            }`}
          >
            <p>{msg.text}</p>

            {/* Show sources only for real bot responses, not thinking message */}
            {msg.sourceReferences &&
              msg.sourceReferences.length > 0 &&
              !msg.isThinking && (
                <div className={styles.sourceReferences}>
                  <strong>Sources:</strong>
                  <ul>
                    {msg.sourceReferences.map((source, index) => (
                      <li key={index}>{source}</li>
                    ))}
                  </ul>
                </div>
              )}
          </div>
        ))}
      </div>

      <div className={styles.inputArea}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !isLoading) {
              handleSendMessage();
            }
          }}
          placeholder="Ask a question about the textbook..."
          className={styles.textInput}
          disabled={isLoading} // Disable input while thinking
        />
        <button
          onClick={handleSendMessage}
          className={styles.sendButton}
          disabled={isLoading}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
}

export default Chatbot;