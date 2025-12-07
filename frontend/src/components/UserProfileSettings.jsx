import React, { useState, useEffect } from 'react';

function UserProfileSettings() {
  const [userId, setUserId] = useState('guest'); // Placeholder for actual user ID
  const [learningStyle, setLearningStyle] = useState('');
  const [preferences, setPreferences] = useState('{\n  "theme": "light",\n  "notifications": true\n}');
  const [message, setMessage] = useState('');

  // In a real app, you'd fetch user profile on component mount
  useEffect(() => {
    // Mock fetching existing user profile
    const fetchUserProfile = async () => {
      // const response = await fetch(`/api/user/${userId}/profile`);
      // const data = await response.json();
      // setLearningStyle(data.learning_style || '');
      // setPreferences(JSON.stringify(data.preferences || {}, null, 2));
      console.log('Mock: User profile fetched');
    };
    fetchUserProfile();
  }, [userId]);

  const handleSavePreferences = async () => {
    try {
      // In a real app, you'd send this to your backend
      // const response = await fetch(`/api/user/${userId}/profile`, {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify({
      //     learning_style: learningStyle,
      //     preferences: JSON.parse(preferences),
      //   }),
      // });
      // if (!response.ok) {
      //   throw new Error(`HTTP error! status: ${response.status}`);
      // }
      setMessage('Preferences saved successfully!');
      console.log('Mock: Preferences saved', { learningStyle, preferences });
    } catch (error) {
      setMessage(`Error saving preferences: ${error.message}`);
      console.error('Error saving preferences:', error);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto' }}>
      <h1>User Profile Settings</h1>
      {message && <p style={{ color: 'green' }}>{message}</p>}

      <div>
        <label htmlFor="learningStyle">Learning Style:</label>
        <select
          id="learningStyle"
          value={learningStyle}
          onChange={(e) => setLearningStyle(e.target.value)}
          style={{ width: '100%', padding: '8px', margin: '10px 0' }}
        >
          <option value="">Select a style</option>
          <option value="visual">Visual</option>
          <option value="auditory">Auditory</option>
          <option value="kinesthetic">Kinesthetic</option>
        </select>
      </div>

      <div>
        <label htmlFor="preferences">Other Preferences (JSON):</label>
        <textarea
          id="preferences"
          value={preferences}
          onChange={(e) => setPreferences(e.target.value)}
          rows="10"
          style={{ width: '100%', padding: '8px', margin: '10px 0' }}
        ></textarea>
      </div>

      <button
        onClick={handleSavePreferences}
        style={{
          padding: '10px 20px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        Save Preferences
      </button>
    </div>
  );
}

export default UserProfileSettings;
