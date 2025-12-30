import { v4 as uuidv4 } from 'uuid';

// Determine API base URL based on the current environment
// For local development: use localhost
// For Hugging Face Spaces or other deployments: use relative path or the same host
const getApiBaseUrl = () => {
  // Check if we're running locally (development)
  const isLocalhost = window.location.hostname === 'localhost' ||
                     window.location.hostname === '127.0.0.1' ||
                     window.location.hostname === '';

  if (isLocalhost) {
    return 'http://localhost:8000/api/v1';
  } else {
    // For deployed environments (Hugging Face Spaces, etc.), use the same origin
    return `${window.location.origin}/api/v1`;
  }
};

const API_BASE_URL = getApiBaseUrl();

export const sendChatQuery = async (queryText, userId = null, context = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: uuidv4(), // Generate a unique ID for the user query
        text: queryText,
        user_id: userId,
        context: context,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to get chatbot response');
    }

    const data = await response.json();
    return data; // Returns ChatbotResponse model
  } catch (error) {
    console.error("Error sending chat query:", error);
    throw error;
  }
};
