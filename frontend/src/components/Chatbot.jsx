import React, { useState } from 'react';
import { sendChatQuery } from '../services/chatbot_api';
import styles from './Chatbot.module.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Tracks if bot is processing

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    // Add user's message
    const userMessage = { id: Date.now(), text: input, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);

    // Show "Thinking..." message
    setIsLoading(true);
    const thinkingMessageId = Date.now() + 1;
    const thinkingMessage = {
      id: thinkingMessageId,
      text: 'Thinking...',
      sender: 'bot',
      isThinking: true,
    };
    setMessages((prev) => [...prev, thinkingMessage]);

    try {
      const data = await sendChatQuery(input);

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

      // Replace thinking message with error
      setMessages((prev) =>
        prev
          .filter((msg) => msg.id !== thinkingMessageId)
          .concat({
            id: Date.now() + 2,
            text: 'Error: Could not get a response from the chatbot.',
            sender: 'bot',
          })
      );
    } finally {
      setIsLoading(false); // Stop loading state
    }

    setInput(''); // Clear input field
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