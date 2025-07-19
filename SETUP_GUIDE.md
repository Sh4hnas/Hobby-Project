# Voice Assistant Setup Guide

This guide provides detailed instructions for setting up and configuring the Voice Assistant on different platforms.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Instructions](#installation-instructions)
- [Configuration](#configuration)
- [Platform-Specific Setup](#platform-specific-setup)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

## System Requirements

### Minimum Requirements

- **Python**: 3.7 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 500MB free space
- **Internet**: Required for speech recognition and AI features
- **Microphone**: Any USB or built-in microphone
- **Speakers/Headphones**: For audio output

### Supported Platforms

- **Windows**: 10, 11 (64-bit)
- **macOS**: 10.14 (Mojave) or later
- **Linux**: Ubuntu 18.04+, Debian 10+, CentOS 7+, Fedora 30+

## Installation Instructions

### Step 1: Python Installation

#### Windows
```bash
# Download Python from https://python.org/downloads/
# Ensure "Add Python to PATH" is checked during installation
# Verify installation:
python --version
pip --version
```

#### macOS
```bash
# Using Homebrew (recommended):
brew install python

# Or download from https://python.org/downloads/
# Verify installation:
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

#### Linux (CentOS/RHEL/Fedora)
```bash
# CentOS/RHEL:
sudo yum install python3 python3-pip

# Fedora:
sudo dnf install python3 python3-pip

python3 --version
pip3 --version
```

### Step 2: System Dependencies

#### Windows
```bash
# No additional system dependencies required
# Audio drivers should be installed automatically
```

#### macOS
```bash
# Install Xcode command line tools:
xcode-select --install

# Install PortAudio (for pyaudio):
brew install portaudio
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y \
    portaudio19-dev \
    python3-pyaudio \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    espeak \
    espeak-data
```

#### Linux (CentOS/RHEL)
```bash
# Enable EPEL repository first:
sudo yum install epel-release

sudo yum install -y \
    portaudio-devel \
    alsa-lib-devel \
    gcc-c++ \
    python3-devel \
    espeak
```

#### Linux (Fedora)
```bash
sudo dnf install -y \
    portaudio-devel \
    alsa-lib-devel \
    gcc-c++ \
    python3-devel \
    espeak
```

### Step 3: Python Dependencies

#### Create Virtual Environment (Recommended)
```bash
# Create virtual environment:
python3 -m venv voice_assistant_env

# Activate virtual environment:
# Windows:
voice_assistant_env\Scripts\activate
# macOS/Linux:
source voice_assistant_env/bin/activate
```

#### Install Dependencies
```bash
# Install from requirements.txt:
pip install -r requirements.txt

# Or install individually:
pip install pyttsx3==2.90
pip install SpeechRecognition==3.10.0
pip install pyjokes==0.6.0
pip install google-generativeai==0.3.2
pip install pyaudio==0.2.11
```

#### Alternative Installation Methods

##### Using pip with specific versions:
```bash
pip install --upgrade pip
pip install pyttsx3 speechrecognition pyjokes google-generativeai pyaudio
```

##### Using conda (if you prefer conda):
```bash
conda create -n voice_assistant python=3.9
conda activate voice_assistant
conda install -c conda-forge pyaudio
pip install pyttsx3 speechrecognition pyjokes google-generativeai
```

## Configuration

### Step 1: Google Gemini API Setup

1. **Get API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated API key

2. **Configure API Key**:

   **Method 1: Environment Variable (Recommended)**
   ```bash
   # Windows (Command Prompt):
   set GEMINI_API_KEY=your_api_key_here
   
   # Windows (PowerShell):
   $env:GEMINI_API_KEY="your_api_key_here"
   
   # macOS/Linux:
   export GEMINI_API_KEY="your_api_key_here"
   
   # Make it permanent by adding to your shell profile:
   echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

   **Method 2: .env File**
   ```bash
   # Create .env file in project directory:
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   
   # Install python-dotenv:
   pip install python-dotenv
   ```

   **Method 3: Direct Code Modification (Not Recommended)**
   ```python
   # Edit project1.py and replace:
   genai.configure(api_key="your_api_key_here")
   ```

### Step 2: Audio Configuration

#### Test Microphone
```python
# Test script - save as test_microphone.py:
import speech_recognition as sr

def test_microphone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Available microphones:")
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"{i}: {microphone_name}")
        
        print("\nAdjusting for ambient noise... Please wait.")
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        
        try:
            audio = r.listen(source, timeout=5)
            print("Recognizing...")
            text = r.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")

if __name__ == "__main__":
    test_microphone()
```

#### Configure Specific Microphone
```python
# If you need to use a specific microphone:
import speech_recognition as sr

# List available microphones:
for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {microphone_name}")

# Use specific microphone by index:
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)  # Use microphone at index 1
```

### Step 3: Text-to-Speech Configuration

#### Test TTS
```python
# Test script - save as test_tts.py:
import pyttsx3

def test_tts():
    engine = pyttsx3.init()
    
    # List available voices:
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} - {voice.id}")
    
    # Test speech:
    engine.say("Hello! Text to speech is working correctly.")
    engine.runAndWait()
    
    # Test different voice (if available):
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
        engine.say("This is a different voice.")
        engine.runAndWait()

if __name__ == "__main__":
    test_tts()
```

## Platform-Specific Setup

### Windows Setup

#### Additional Windows Configuration:
```bash
# Install Microsoft Visual C++ Redistributable if needed:
# Download from: https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

# Set up Windows Speech Platform (optional, for better TTS):
# Download and install:
# - Microsoft Speech Platform Runtime (x64)
# - Microsoft Speech Platform SDK (x64)
```

#### Windows-Specific Issues:
```python
# If you get SSL errors, try:
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# For Windows-specific audio issues:
pip install pywin32
```

### macOS Setup

#### macOS-Specific Configuration:
```bash
# Grant microphone permissions:
# System Preferences > Security & Privacy > Privacy > Microphone
# Add Terminal and/or your Python IDE

# Install additional audio libraries:
brew install sox libsox-fmt-all

# For M1 Macs, you might need:
arch -arm64 brew install portaudio
arch -arm64 pip install pyaudio
```

### Linux Setup

#### Ubuntu/Debian Additional Setup:
```bash
# Install additional audio tools:
sudo apt install -y \
    pulseaudio \
    pulseaudio-utils \
    alsa-utils \
    sox \
    libsox-fmt-all

# Configure PulseAudio (if needed):
pulseaudio --start
pactl info

# Test audio:
speaker-test -t sine -f 1000 -l 1
arecord -d 3 test.wav && aplay test.wav
```

#### CentOS/RHEL/Fedora Additional Setup:
```bash
# Install additional packages:
sudo yum install -y pulseaudio pulseaudio-utils alsa-utils sox
# or for Fedora:
sudo dnf install -y pulseaudio pulseaudio-utils alsa-utils sox

# Start audio services:
systemctl --user start pulseaudio
```

#### Fix Common Linux Issues:
```bash
# If you get permission errors for audio devices:
sudo usermod -a -G audio $USER
# Then log out and back in

# If microphone doesn't work:
alsamixer  # Unmute and adjust microphone levels

# For virtual environments on Linux:
sudo apt install python3.x-venv  # Replace x with your Python version
```

## Troubleshooting

### Common Installation Issues

#### PyAudio Installation Problems:

**Windows:**
```bash
# If pip install pyaudio fails:
pip install pipwin
pipwin install pyaudio

# Or download wheel file:
# Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Download appropriate .whl file and install:
pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
```

**macOS:**
```bash
# If pyaudio installation fails:
brew install portaudio
pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio

# For M1 Macs:
CPPFLAGS=-I/opt/homebrew/include LDFLAGS=-L/opt/homebrew/lib pip install pyaudio
```

**Linux:**
```bash
# If pyaudio installation fails:
sudo apt install python3-dev
pip install pyaudio

# Alternative:
sudo apt install python3-pyaudio
```

#### Speech Recognition Issues:

```python
# Test internet connection for Google Speech API:
import requests
try:
    response = requests.get("https://www.google.com", timeout=5)
    print("Internet connection: OK")
except:
    print("Internet connection: Failed")

# Test with different recognition engines:
import speech_recognition as sr
r = sr.Recognizer()
# Try offline recognition (requires additional setup):
# r.recognize_sphinx(audio)  # CMU Sphinx
# r.recognize_wit(audio, key="WIT_AI_KEY")  # Wit.ai
```

#### API Key Issues:

```bash
# Verify API key is set:
python -c "import os; print('API Key:', os.getenv('GEMINI_API_KEY'))"

# Test API key:
python -c "
import google.generativeai as genai
import os
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Hello')
print(response.text)
"
```

### Runtime Issues

#### Microphone Not Working:
```bash
# Check microphone devices:
python -c "
import speech_recognition as sr
print('Microphones:')
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{i}: {name}')
"

# Test microphone access:
python -c "
import speech_recognition as sr
r = sr.Recognizer()
try:
    with sr.Microphone() as source:
        print('Microphone access: OK')
        r.adjust_for_ambient_noise(source, duration=1)
        print('Noise adjustment: OK')
except Exception as e:
    print(f'Microphone error: {e}')
"
```

#### TTS Not Working:
```bash
# Test TTS engines:
python -c "
import pyttsx3
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f'Available voices: {len(voices)}')
    for voice in voices:
        print(f'  {voice.name}: {voice.id}')
    engine.say('Test')
    engine.runAndWait()
    print('TTS: OK')
except Exception as e:
    print(f'TTS error: {e}')
"
```

#### Performance Issues:
```python
# Monitor resource usage:
import psutil
import threading
import time

def monitor_resources():
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        print(f"CPU: {cpu}%, Memory: {memory.percent}%")
        time.sleep(5)

# Run in background:
monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
monitor_thread.start()
```

## Advanced Configuration

### Custom Voice Configuration

```python
# Advanced TTS configuration:
import pyttsx3

def configure_voice():
    engine = pyttsx3.init()
    
    # Get current settings:
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')
    voice = engine.getProperty('voice')
    
    print(f"Current rate: {rate}")
    print(f"Current volume: {volume}")
    print(f"Current voice: {voice}")
    
    # Customize settings:
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    
    # Select voice by gender/language:
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
    return engine
```

### Custom Audio Configuration

```python
# Advanced microphone configuration:
import speech_recognition as sr
import pyaudio

def configure_microphone():
    # List all audio devices:
    p = pyaudio.PyAudio()
    print("Audio devices:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"{i}: {info['name']} - {info['maxInputChannels']} channels")
    
    # Configure recognizer with custom settings:
    r = sr.Recognizer()
    r.energy_threshold = 300  # Minimum audio energy
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8  # Seconds of non-speaking audio before phrase is complete
    r.phrase_threshold = 0.3  # Minimum seconds of speaking audio before we consider the speaking audio a phrase
    r.non_speaking_duration = 0.5  # Seconds of non-speaking audio to keep on both sides of the recording
    
    return r

def use_custom_microphone():
    r = configure_microphone()
    # Use specific microphone:
    mic = sr.Microphone(device_index=1)  # Change index as needed
    
    with mic as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=2)
        print("Listening...")
        audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
```

### Environment File Template

Create a `.env` file with the following template:

```env
# Google Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Other API Keys
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key

# Audio Configuration
DEFAULT_MICROPHONE_INDEX=0
DEFAULT_VOICE_INDEX=0
SPEECH_RATE=150
SPEECH_VOLUME=0.9

# Application Settings
DEBUG_MODE=false
LOG_LEVEL=INFO
CACHE_RESPONSES=true
CACHE_TIMEOUT=300

# Music Directory (for song command)
MUSIC_DIRECTORY=/home/user/Music
```

### Systemd Service (Linux)

Create a systemd service to run the voice assistant as a service:

```bash
# Create service file:
sudo nano /etc/systemd/system/voice-assistant.service
```

```ini
[Unit]
Description=Voice Assistant Service
After=network.target sound.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/voice/assistant
Environment=PATH=/path/to/voice/assistant/venv/bin
ExecStart=/path/to/voice/assistant/venv/bin/python project1.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service:
sudo systemctl daemon-reload
sudo systemctl enable voice-assistant.service
sudo systemctl start voice-assistant.service

# Check status:
sudo systemctl status voice-assistant.service
```

### Docker Configuration

Create a Dockerfile for containerized deployment:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    espeak \
    espeak-data \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables
ENV GEMINI_API_KEY=""
ENV PYTHONUNBUFFERED=1

# Expose volume for audio devices
VOLUME ["/dev/snd"]

# Run the application
CMD ["python", "project1.py"]
```

```bash
# Build and run Docker container:
docker build -t voice-assistant .
docker run -it --device /dev/snd -e GEMINI_API_KEY="your_key" voice-assistant
```

---

*Voice Assistant Setup Guide - Version 1.0*
*Complete installation and configuration guide for all supported platforms*