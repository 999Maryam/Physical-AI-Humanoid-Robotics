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

// Helper function: exponential backoff delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Helper function: calculate backoff delay
const getBackoffDelay = (attempt) => {
  // Exponential backoff: 1s, 2s, 4s, 8s, 16s
  return Math.min(1000 * Math.pow(2, attempt), 16000);
};

// Main API call with retry logic for 429 errors
export const sendChatQuery = async (queryText, userId = null, context = null, onRetry = null) => {
  const maxRetries = 3;
  let lastError = null;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
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

      // Handle 429 rate limit errors with retry
      if (response.status === 429) {
        lastError = new Error('RATE_LIMIT');
        lastError.statusCode = 429;

        if (attempt < maxRetries) {
          const backoffTime = getBackoffDelay(attempt);
          console.log(`Rate limit hit, retrying in ${backoffTime}ms (attempt ${attempt + 1}/${maxRetries})...`);

          // Notify caller about retry (for UI updates)
          if (onRetry) {
            onRetry(attempt + 1, maxRetries, backoffTime);
          }

          await delay(backoffTime);
          continue; // Retry
        } else {
          throw lastError; // Max retries exceeded
        }
      }

      // Handle other HTTP errors
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const error = new Error(errorData.detail || `HTTP error ${response.status}`);
        error.statusCode = response.status;
        throw error;
      }

      const data = await response.json();
      return data; // Success - Returns ChatbotResponse model

    } catch (error) {
      // Network errors or JSON parsing errors
      if (error.statusCode === 429) {
        lastError = error;
        if (attempt < maxRetries) {
          const backoffTime = getBackoffDelay(attempt);
          console.log(`Rate limit error, retrying in ${backoffTime}ms (attempt ${attempt + 1}/${maxRetries})...`);

          if (onRetry) {
            onRetry(attempt + 1, maxRetries, backoffTime);
          }

          await delay(backoffTime);
          continue;
        }
      }

      // For non-429 errors or max retries exceeded, throw immediately
      console.error("Error sending chat query:", error);
      throw error;
    }
  }

  // If we get here, all retries failed
  throw lastError || new Error('Failed to get chatbot response after retries');
};
