import React, { useState } from 'react';
import { sendChatQuery } from '../services/chatbot_api';
import styles from './Chatbot.module.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const newUserMessage = { id: Date.now(), text: input, sender: 'user' };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);

    try {
      const data = await sendChatQuery(input);
      const newBotMessage = { id: Date.now() + 1, text: data.text, sender: 'bot', sourceReferences: data.source_references };
      setMessages((prevMessages) => [...prevMessages, newBotMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { id: Date.now() + 1, text: 'Error: Could not get a response from the chatbot.', sender: 'bot' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }

    setInput('');
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.messagesList}>
        {messages.map((msg) => (
          <div key={msg.id} className={`${styles.message} ${styles[msg.sender]}`}>
            <p>{msg.text}</p>
            {msg.sourceReferences && msg.sourceReferences.length > 0 && (
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
            if (e.key === 'Enter') {
              handleSendMessage();
            }
          }}
          placeholder="Ask a question about the textbook..."
          className={styles.textInput}
        />
        <button onClick={handleSendMessage} className={styles.sendButton}>Send</button>
      </div>
    </div>
  );
}

export default Chatbot;
