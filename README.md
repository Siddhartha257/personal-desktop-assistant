# Luna - Voice-Controlled Desktop Assistant for macOS

## Description
Luna is an intelligent voice-controlled desktop assistant built specifically for macOS. It combines the power of Google's Gemini AI with voice recognition to create a seamless and interactive experience. Luna can help you perform basic tasks through natural language commands, though it currently has a limited set of features focused on essential functionality.

## Key Features
- 🎤 Voice Command Recognition (macOS native)
- 🤖 AI-Powered Conversations using Google Gemini
- 🌐 Basic Web Search and Navigation
- 📰 Real-time News Updates
- ⏰ Time and Date Information
- 📂 Basic File and Application Management
- 📚 Wikipedia Knowledge Base
- 🎵 Basic Media Control (YouTube)

## System Requirements
- macOS operating system
- Python 3.x
- Working microphone
- Internet connection
- API keys for Gemini AI and News API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Luna.git
cd Luna
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up API Keys:
Create a `sk.py` file in the project root and add your API keys:
```python
GEMINI_API_KEY = "your_gemini_api_key"
NEWS_API_KEY = "your_news_api_key"
```

## Usage

1. Start Luna:
```bash
python main.py
```

2. Voice Commands Examples:
- "Hey Luna, what time is it?"
- "Open Chrome"
- "Search for Python tutorials on YouTube"
- "Tell me about artificial intelligence"
- "What's the latest news about technology?"
- "Find file documents"
- "Open Spotify"

## Limitations
- Currently only supports macOS
- Limited set of voice commands
- Basic application control (only supports predefined applications)
- Limited file system access
- Basic web search capabilities
- No system-level modifications
- No background process management
- Limited media control features

## Technologies Used

### Core Technologies
- Python 3.x
- Google Gemini AI
- macOS Speech Recognition
- Natural Language Processing (spaCy)

### Key Libraries
- `google-generativeai` - For AI-powered conversations
- `SpeechRecognition` - For voice command processing
- `spacy` - For natural language understanding
- `requests` - For API communications
- `wikipedia` - For knowledge base queries
- `PyAudio` - For audio input processing
- `numpy` - For numerical operations

## Features in Detail

### Voice Recognition
- macOS native voice command processing
- Basic natural language understanding

### AI Integration
- Powered by Google's Gemini AI
- Basic context-aware conversations
- Simple response generation

### Web Integration
- Basic YouTube search
- Simple Google search capabilities
- Wikipedia knowledge queries
- Basic news updates

### System Control
- Limited application launching (predefined list)
- Basic file system navigation
- Time and date information
- No system-level modifications

### Media Control
- Basic YouTube video search
- No direct media player control
- Limited web browser automation

## Acknowledgments
- Google Gemini AI for providing the AI capabilities
- The open-source community for the various libraries used
- macOS for native speech recognition capabilities 
