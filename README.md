# Learning Path Generator with Model Context Protocol (MCP)

This project is a Streamlit-based web application that generates personalized learning paths using the Model Context Protocol (MCP). It integrates with various services including YouTube, Google Drive, and Notion to create comprehensive learning experiences.

## Features

- 🎯 Generate personalized learning paths based on your goals
- 🎥 Integration with YouTube for video content
- 📁 Google Drive integration for document storage
- 📝 Notion integration for note-taking and organization
- 🚀 Real-time progress tracking
- 🎨 User-friendly Streamlit interface

## Prerequisites

- Python 3.10+
- Google ai Studio API Key
- Pipedream URLs for integrations (YouTube and either Drive or Notion)

## Installation

1. Clone the repository:

2. Create and activate a virtual environment:

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

Before running the application, you'll need to set up:

1. Google API Key
2. Pipedream URLs for:
   - YouTube (required)
   - Google Drive or Notion (based on your preference)

## Running the Application

To start the learning path application, run:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501` by default.

## Usage

1. Enter your Google ai studio API key and Pipedream URLs in the sidebar
2. Select your preferred secondary tool (Drive or Notion)
3. Enter your learning goal (e.g., "I want to learn python basics in 3 days")
4. Click "Generate Learning Path" to create your personalized learning plan

## New: Video Interview System (MIP Prototype)

Added a minimal end-to-end prototype for a video interview evaluation system that analyzes visual, audio, and textual signals and produces a combined predictive score.

### Features
- Visual analysis: lightweight face movement proxy, gaze engagement, emotion heuristics
- Audio analysis: speech activity ratio, approximate pitch, speech rate, timbre brightness (best-effort using `ffmpeg` + `librosa`)
- Text analysis: heuristic DISC estimation, intrinsic traits, sentiment, clarity, keywords
- Combined scoring with an interpretable breakdown

### Run the Interview App
```bash
pip install -r requirements.txt
streamlit run interview_app.py
```

Upload a video file and optionally paste transcript text. The app will display all analyses and a combined score.

Notes:
- Audio analysis requires `ffmpeg` installed on your system and available in PATH.
- If optional deps are missing, the app falls back to safe defaults, so it still runs.

## Project Structure

- `app.py` - Main Streamlit application (learning path)
- `interview_app.py` - Video Interview System UI
- `analyzers/` - Video, audio, text analyzers
- `scoring.py` - Combined scoring logic
- `utils.py` - Utility functions and helper methods
- `prompt.py` - Prompt template
- `requirements.txt` - Project dependencies
