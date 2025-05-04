# Gift Recommender From Chat

An application that recommends gift ideas for friends based on chat history.

## Overview

This application allows users to upload chat history files and receive personalized gift recommendations based on the content.

## Project Structure

- `frontend/`: React + TypeScript frontend built with Vite and Chakra UI
- `backend/`: FastAPI backend for processing chat history and generating recommendations

## Setup Instructions

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. The frontend will be available at http://localhost:5173

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the setup script (creates virtual environment and installs dependencies):
   ```bash
   ./run.sh
   ```

3. The backend API will be available at http://localhost:8000

4. API documentation will be available at http://localhost:8000/docs

## How to Use

1. Start both the frontend and backend servers
2. Open the frontend application in your browser
3. Upload a chat history file (text, JSON, or CSV format)
4. Click "Analyze Chat & Get Recommendations"
5. View the generated gift recommendations

## Development

The current implementation includes:
- File upload with drag & drop support
- Frontend UI with Chakra UI components
- Backend API with file validation and mock recommendations
