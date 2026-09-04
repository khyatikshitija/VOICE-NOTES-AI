VOICE NOTES AI
It's a simple AI powered voice notes assistant that helps to convert the spoken notes into text and automatically organises them into simple and concise summary and actionable tasks.

FEATURES
1. Record a voice note directly in the browser
2. Upload audio files (MP3,WAV,M4A,WEBM)
3. Speech to text transcription using FASTER-WHISPER
4. Automatic language detection
5. Ai-generated summary and action items when an OpenAI API KEY is cofigured
6. Local fallback summary and action-item extraction when an API key is unavailable
7. Action items displayed as interactive checkboxes
8. Start a new voice note without restarting the application
9. Handles audio conversion failures and empty/silent recordings

TECHNOLOGY USED
1. Python
2. Streamlit
3. Faster-Whisper
4. OpenAI API
5. FFmpeg
6. audio-recorder-streamlit
7. Python-dotenv

WORKING
Voice Recording / Audio Upload
            ↓
       FFmpeg Conversion
            ↓
      Faster-Whisper
            ↓
   Language Detection + Text
            ↓
     Summary + Action Items
            ↓
       Simple Streamlit UI

HOW TO RUN:

1. Clone or download the project
Open the project folder in VS Code.

2. Create a virtual environment
python -m venv venv

3. Install dependencies
venv\Scripts\python.exe -m pip install -r requirements.txt

4. Install FFmpeg
FFmpeg is required to convert uploaded or recorded audio into WAV format for transcription.

5. Configure OpenAI API
Create a ".env" file in the project root:

OPENAI_API_KEY=your_api_key_here
The application also works without an OpenAI API key by using a local fallback for summary and action-item extraction.

6. Start the application
venv\Scripts\python.exe -m streamlit run app\main.py

The application will open in your browser.

ERROR HANDLING
The application handles:

- Unsupported or problematic audio conversion
- Silent recordings / no speech detected
- Missing OpenAI API key
- Different input audio formats
- New-note/reset workflow

PROJECT GOAL
The main goal of this project is to convert the unstructured voice thoughts into an organised and useful notes with minimal user effort

FUTURE IMPROVEMENTS:
- Better multilingual transcription accuracy
- Speaker identification
- Persistent note history
- Export notes to PDF or text
- Improved AI categorization
- Cloud deployment
- Search across previous voice notes
- try to make transcription more faster
- Make it more attractive and engaging

PROJECT 
VOICE NOTES AI- Take home assessment project
