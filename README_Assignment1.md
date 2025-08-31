# Assignment 1: PDF to Speech Conversion System

This project implements a comprehensive PDF to Speech conversion system with two main functionalities:

## 🎯 Features

### 1. 🔊 Simple PDF to Speech (gTTS)

- Convert PDF documents to speech using Google Text-to-Speech
- Support for multiple languages
- Fast conversion with internet connection
- Adjustable speech speed

### 2. 🎭 PDF to Speech with Voice Cloning (Coqui TTS)

- Clone any voice from a reference sample
- Convert PDF text using the cloned voice
- AI-powered neural voice synthesis
- High-quality, natural-sounding speech

### 3. 🧹 Voice Sample Enhancement

- **Noise Reduction**: Remove background noise from voice samples
- **Audio Normalization**: Adjust volume levels
- **Frequency Filtering**: Remove unwanted low/high frequencies
- **Silence Trimming**: Remove silent parts from beginning/end

## 📁 Files Structure

```
TTS/
├── Assignment1.py          # Main functions library
├── streamlit_app.py        # Web interface
├── demo.py                 # Command-line demo
├── life_3_0.pdf           # Sample PDF
├── Waleed.wav             # Sample voice for cloning
└── README.md              # This file
```

## 🚀 Quick Start

### Installation

```bash
# Activate your virtual environment
& "D:/Gen AI/venv39/Scripts/Activate.ps1"

# Install required packages
pip install gtts TTS streamlit noisereduce librosa soundfile PyMuPDF
```

### Option 1: Web Interface (Recommended)

```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501`

### Option 2: Command Line Demo

```bash
python demo.py
```

### Option 3: Use Functions Directly

```python
from Assignment1 import convert_pdf_to_speech_gtts, convert_pdf_to_speech_voice_clone

# Simple gTTS conversion
convert_pdf_to_speech_gtts("document.pdf", "output.mp3", language="en")

# Voice cloning conversion
convert_pdf_to_speech_voice_clone("document.pdf", "voice_sample.wav", "cloned_output.wav")
```

## 📚 Function Reference

### Core Functions

#### `convert_pdf_to_speech_gtts(pdf_path, output_path, language='en', page_range=None, slow=False)`

Convert PDF to speech using Google TTS.

- **pdf_path**: Path to PDF file
- **output_path**: Where to save audio (MP3)
- **language**: Language code (en, es, fr, etc.)
- **page_range**: Tuple (start, end) for specific pages
- **slow**: Slower speech pace

#### `convert_pdf_to_speech_voice_clone(pdf_path, reference_voice_path, output_path, page_range=None, clean_voice=False)`

Convert PDF using voice cloning.

- **pdf_path**: Path to PDF file
- **reference_voice_path**: Voice sample for cloning
- **output_path**: Where to save audio (WAV)
- **page_range**: Tuple (start, end) for specific pages
- **clean_voice**: Apply voice enhancement

#### `clean_voice_sample(voice_path, output_path=None, reduce_noise=True, normalize_audio=True, apply_filters=True)`

Enhance voice sample quality.

- **voice_path**: Input voice file
- **output_path**: Where to save cleaned audio
- **reduce_noise**: Remove background noise
- **normalize_audio**: Adjust volume levels
- **apply_filters**: Apply frequency filters

### Utility Functions

#### `extract_text_from_pdf(pdf_path, page_range=None)`

Extract text from PDF pages.

#### `get_pdf_info(pdf_path)`

Get PDF metadata (page count, title, author, etc.).

## 🎛️ Streamlit App Features

### Simple TTS Tab

- 📄 Upload PDF files
- 🌐 Select language (10+ supported)
- 📄 Choose specific page ranges
- 🐌 Adjust speech speed
- 💾 Download generated audio

### Voice Cloning Tab

- 📄 Upload PDF documents
- 🎤 Upload voice samples (WAV/MP3)
- ✨ Optional voice cleaning
- 📊 Progress tracking
- 🎵 Audio preview
- 💾 Download cloned speech

## 🔧 Voice Sample Guidelines

For best voice cloning results:

- **Duration**: 10-30 seconds of clear speech
- **Quality**: High quality, minimal background noise
- **Content**: Natural speech with varied intonation
- **Format**: WAV preferred, MP3/FLAC supported

## 📊 Performance Notes

### gTTS Conversion

- **Speed**: Very fast (< 1 second per page)
- **Quality**: Good, robotic but clear
- **Requirements**: Internet connection
- **Languages**: 50+ supported

### Voice Cloning

- **Speed**: Moderate (10-30 seconds per page)
- **Quality**: High, natural-sounding
- **Requirements**: Local processing (GPU recommended)
- **Languages**: 6 main languages supported

### Voice Cleaning

- **Processing**: 2-5 seconds per sample
- **File Size**: Usually reduced by 40-60%
- **Quality**: Significantly improved clarity

## 🛠️ Dependencies

### Core Requirements

```
PyMuPDF>=1.23.0    # PDF processing
gtts>=2.5.0         # Google Text-to-Speech
TTS>=0.22.0         # Coqui TTS for voice cloning
librosa>=0.10.0     # Audio processing
soundfile>=0.12.0   # Audio I/O
numpy>=1.22.0       # Numerical operations
```

### Optional Enhancements

```
noisereduce>=3.0.0  # Noise reduction
scipy>=1.10.0       # Advanced filtering
streamlit>=1.49.0   # Web interface
```

## 🐛 Troubleshooting

### Common Issues

**"No text found in PDF"**

- Try different page ranges
- Some PDFs have non-extractable text (images)
- Use OCR tools for scanned documents

**"TTS model loading failed"**

- Check internet connection for model download
- Ensure sufficient disk space (2-3 GB)
- Try restarting the application

**"Voice cloning slow on CPU"**

- Expected behavior without GPU
- Consider using gTTS for faster results
- Use shorter text passages for testing

**Numpy version conflicts**

- Use `numpy==1.23.0` for compatibility
- Some warnings are normal and don't affect functionality

### Performance Tips

1. **For large PDFs**: Process in smaller page ranges
2. **For better quality**: Use high-quality voice samples (16-22kHz)
3. **For speed**: Use gTTS for quick prototypes
4. **For production**: Consider GPU acceleration for voice cloning

## 📝 Example Usage

### Basic PDF to Speech

```python
# Convert entire document
convert_pdf_to_speech_gtts("book.pdf", "audiobook.mp3")

# Convert specific chapters (pages 50-75)
convert_pdf_to_speech_gtts("book.pdf", "chapter3.mp3", page_range=(49, 74))

# Spanish audiobook
convert_pdf_to_speech_gtts("libro.pdf", "audiolibro.mp3", language="es")
```

### Voice Cloning

```python
# Clone voice and convert PDF
convert_pdf_to_speech_voice_clone(
    "document.pdf",
    "my_voice.wav",
    "personalized_audio.wav",
    clean_voice=True
)

# Convert with cleaned voice sample
cleaned_voice = clean_voice_sample("noisy_voice.wav")
convert_pdf_to_speech_voice_clone("doc.pdf", cleaned_voice, "output.wav")
```

## 🚀 Advanced Usage

### Batch Processing

```python
import os
from Assignment1 import convert_pdf_to_speech_gtts

# Convert all PDFs in a directory
pdf_dir = "documents/"
for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith('.pdf'):
        input_path = os.path.join(pdf_dir, pdf_file)
        output_path = f"audio_{pdf_file[:-4]}.mp3"
        convert_pdf_to_speech_gtts(input_path, output_path)
```

### Custom Voice Enhancement

```python
# Advanced voice cleaning
clean_voice_sample(
    "raw_voice.wav",
    "enhanced_voice.wav",
    reduce_noise=True,
    normalize_audio=True,
    apply_filters=True
)
```

## 📞 Support

For issues or questions:

1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Test with the provided demo files first
4. Check console output for detailed error messages

---

**Created for Assignment 1 - PDF to Speech Conversion System**  
_Features both simple TTS and advanced voice cloning capabilities_
