import { v4 as uuidv4 } from 'uuid';

const API_BASE_URL = 'http://localhost:8000/api/v1'; // Adjust if your FastAPI runs on a different port/path

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
