import axios from 'axios';

// Define the base URL for the FastAPI backend
const API_BASE_URL = 'http://localhost:8000';

// Define the response type for gift recommendations
export interface GiftIdea {
  name: string;
  description: string;
  link: string;
}

export interface GiftRecommendations {
  notes: string;
  gift_ideas: GiftIdea[];
}

// API service for communicating with the backend
const apiService = {
  // Upload chat history file and get gift recommendations
  async uploadChatHistory(
    file: File,
    userName: string,
    friendName: string
  ): Promise<GiftRecommendations> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_name', userName);
    formData.append('friend_name', friendName);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/analyze-chat`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      return response.data.recommendations;
    } catch (error) {
      console.error('Error uploading chat history:', error);
      throw error;
    }
  },
};

export default apiService; 