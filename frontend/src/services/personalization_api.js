const API_BASE_URL = 'http://localhost:8000/api/v1'; // Adjust if your FastAPI runs on a different port/path

export const getPersonalizedChapterContent = async (userId, chapterId, originalContent) => {
  try {
    // In a real application, userId would be dynamic
    const response = await fetch(`${API_BASE_URL}/personalize/${userId}/chapter/${chapterId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ original_content: originalContent }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to get personalized content');
    }

    const data = await response.json();
    return data.personalized_content;
  } catch (error) {
    console.error("Error fetching personalized content:", error);
    throw error;
  }
};
