# AI Healthcare Monitoring System

A microservices-based real-time healthcare monitoring application that tracks patient glucose levels, simulates live medical data, and utilizes an AI-driven engine to provide instant medical analysis and voice-assisted conversational feedback.

## Architecture

The system is designed with a modern microservices architecture, fully containerized using Docker.

- Frontend: React (TypeScript), Vite, TailwindCSS, Recharts, Web Speech API (STT & TTS)
- Backend: FastAPI, SQLAlchemy (PostgreSQL)
- AI Engine: CrewAI, Groq (llama-3.1-8b-instant), LiteLLM
- Database: PostgreSQL 15
- Simulator: Python-based real-time data generator

## Key Features

1. Real-Time Dashboard: Visualizes live glucose data streams using Recharts.
2. Data Simulator: Continuously pushes realistic glucose measurements to the backend, simulating a continuous glucose monitor (CGM).
3. AI Medical Analyst: Utilizes CrewAI and Groq's Llama 3 models to analyze historical glucose data and generate structured medical assessments and recommendations.
4. Voice Assistant: Integrated directly into the dashboard. Users can ask questions via microphone, and the AI will analyze the data, provide a concise response, and read it aloud using browser-native Text-to-Speech (TTS).

## Prerequisites

- Docker and Docker Compose
- A valid Groq API Key

## Setup and Installation

1. Clone the repository and navigate to the project directory.

2. Configure the environment variables by modifying the `.env` file in the root directory:
   GROQ_API_KEY=your_api_key_here

3. Build and start the containers using Docker Compose:
   docker-compose up --build -d

4. The following services will be available:
   - Frontend Application: http://localhost:5173
   - Backend API (FastAPI Swagger UI): http://localhost:8000/docs
   - PostgreSQL Database: localhost:5432

## Usage

- Once the containers are running, the Data Simulator will automatically register a default patient (if one does not exist) and begin streaming glucose data every 10 seconds.
- Open the Frontend Application in your browser. The dashboard will automatically update as new data arrives.
- Click "Generate Report" to receive a comprehensive analysis of the recent glucose trends.
- Click the Microphone icon in the AI Analyst section to ask specific questions about the data. The assistant will transcribe your voice, process the query through the LLM, display the response, and read it out loud.

## Project Structure

- /frontend: React/Vite application containing the dashboard components.
- /backend: FastAPI application, database schemas, and CRUD operations.
- /ai: CrewAI configuration, defining agents and analysis tasks.
- /scripts: Python scripts including the real-time data simulator.

## License

This project is licensed under the MIT License.
