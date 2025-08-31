"""
Assignment 1: PDF to Speech Conversion System
============================================

This module provides functions for:
1. Simple PDF to Speech conversion using gTTS
2. PDF to Speech with Voice Cloning using Coqui TTS
3. Optional voice sample cleaning and noise reduction
4. Streamlit-ready functions for easy integration

Functions are designed to be called independently for different use cases.
"""

import os
from typing import Optional, Tuple, List
import tempfile
from pathlib import Path

# Core dependencies
import fitz  # PyMuPDF for PDF processing
import numpy as np
import soundfile as sf
import librosa

# TTS dependencies
try:
    from gtts import gTTS
except ImportError:
    print("Warning: gTTS not installed. Install with: pip install gtts")
    gTTS = None

try:
    from TTS.api import TTS
except ImportError:
    print("Warning: TTS not installed. Install with: pip install TTS")
    TTS = None

# Optional noise reduction dependencies
try:
    import noisereduce as nr
    NOISE_REDUCTION_AVAILABLE = True
except ImportError:
    print("Info: noisereduce not available. Install with: pip install noisereduce")
    NOISE_REDUCTION_AVAILABLE = False

try:
    from scipy.signal import butter, filtfilt
    SCIPY_AVAILABLE = True
except ImportError:
    print("Warning: scipy not available for advanced filtering")
    SCIPY_AVAILABLE = False


def extract_text_from_pdf(pdf_path: str, page_range: Optional[Tuple[int, int]] = None) -> List[str]:
    """
    Extract text from PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        page_range (tuple, optional): (start_page, end_page) to extract specific pages
    
    Returns:
        List[str]: List of text content from each page
    
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        Exception: If PDF cannot be processed
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    try:
        doc = fitz.open(pdf_path)
        pages_text = []
        
        start_page = page_range[0] if page_range else 0
        end_page = page_range[1] if page_range else len(doc) - 1
        
        for page_num in range(start_page, min(end_page + 1, len(doc))):
            page = doc[page_num]
            text = page.get_text().strip()
            if text:  # Only add non-empty pages
                pages_text.append(text)
        
        doc.close()
        return pages_text
        
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")


def clean_voice_sample(
    voice_path: str, 
    output_path: Optional[str] = None,
    reduce_noise: bool = True,
    normalize_audio: bool = True,
    apply_filters: bool = True,
    trim_silence: bool = True
) -> str:
    """
    Clean and enhance voice sample by reducing noise and normalizing.
    
    Args:
        voice_path (str): Path to input voice sample
        output_path (str, optional): Path for cleaned output. If None, creates temp file
        reduce_noise (bool): Apply noise reduction
        normalize_audio (bool): Normalize audio levels
        apply_filters (bool): Apply audio filters
        trim_silence (bool): Trim silence from beginning and end
    
    Returns:
        str: Path to cleaned voice sample
    
    Raises:
        FileNotFoundError: If input voice file doesn't exist
        Exception: If audio processing fails
    """
    if not os.path.exists(voice_path):
        raise FileNotFoundError(f"Voice sample not found: {voice_path}")
    
    try:
        # Load audio
        audio_data, sample_rate = librosa.load(voice_path, sr=None)
        
        # Create output path if not provided
        if output_path is None:
            base_name = Path(voice_path).stem
            output_path = str(Path(voice_path).parent / f"{base_name}_cleaned.wav")
        
        print(f"🔧 Cleaning voice sample: {voice_path}")
        
        # 1. Noise Reduction
        if reduce_noise and NOISE_REDUCTION_AVAILABLE:
            print("   - Applying noise reduction...")
            # Use first 1 second as noise profile
            noise_sample_duration = min(1.0, len(audio_data) / sample_rate / 4)
            noise_sample_length = int(noise_sample_duration * sample_rate)
            
            audio_data = nr.reduce_noise(
                y=audio_data, 
                sr=sample_rate,
                stationary=True,
                prop_decrease=0.8
            )
        
        # 2. Apply filters to remove low/high frequency noise
        if apply_filters and SCIPY_AVAILABLE:
            print("   - Applying audio filters...")
            # High-pass filter to remove low frequency noise (below 80 Hz)
            nyquist = sample_rate / 2
            low_cutoff = 80 / nyquist
            high_cutoff = min(8000 / nyquist, 0.95)  # Low-pass at 8kHz or 95% Nyquist
            
            if low_cutoff < 0.95:
                b, a = butter(2, low_cutoff, btype='high')
                audio_data = filtfilt(b, a, audio_data)
            
            if high_cutoff < 0.95:
                b, a = butter(2, high_cutoff, btype='low')
                audio_data = filtfilt(b, a, audio_data)
        
        # 3. Normalize audio
        if normalize_audio:
            print("   - Normalizing audio levels...")
            # Remove DC offset
            audio_data = audio_data - np.mean(audio_data)
            
            # Normalize to prevent clipping (leave some headroom)
            max_amplitude = np.max(np.abs(audio_data))
            if max_amplitude > 0:
                audio_data = audio_data / max_amplitude * 0.9
        
        # 4. Trim silence from beginning and end
        if trim_silence:
            print("   - Trimming silence...")
            audio_data, _ = librosa.effects.trim(audio_data, top_db=30)
        
        # Save cleaned audio
        sf.write(output_path, audio_data, sample_rate)
        print(f"✅ Cleaned voice sample saved: {output_path}")
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Error cleaning voice sample: {str(e)}")


def convert_pdf_to_speech_gtts(
    pdf_path: str,
    output_path: str,
    language: str = 'en',
    page_range: Optional[Tuple[int, int]] = None,
    slow: bool = False
) -> str:
    """
    Convert PDF to speech using Google Text-to-Speech (gTTS).
    
    Args:
        pdf_path (str): Path to PDF file
        output_path (str): Path for output audio file
        language (str): Language code for TTS (default: 'en')
        page_range (tuple, optional): (start_page, end_page) to convert specific pages
        slow (bool): Speak slowly
    
    Returns:
        str: Path to generated audio file
    
    Raises:
        Exception: If conversion fails
    """
    if gTTS is None:
        raise Exception("gTTS not available. Install with: pip install gtts")
    
    try:
        print(f"📖 Extracting text from PDF: {pdf_path}")
        pages_text = extract_text_from_pdf(pdf_path, page_range)
        
        if not pages_text:
            raise Exception("No text found in PDF")
        
        # Combine all pages text
        full_text = "\n\n".join(pages_text)
        
        print(f"🎙️ Converting to speech using gTTS (language: {language})")
        print(f"   Text length: {len(full_text)} characters")
        
        # Create gTTS object
        tts = gTTS(text=full_text, lang=language, slow=slow)
        
        # Save audio
        tts.save(output_path)
        
        print(f"✅ Speech generated using gTTS: {output_path}")
        return output_path
        
    except Exception as e:
        raise Exception(f"Error in PDF to speech conversion (gTTS): {str(e)}")


def convert_pdf_to_speech_voice_clone(
    pdf_path: str,
    reference_voice_path: str,
    output_path: str,
    page_range: Optional[Tuple[int, int]] = None,
    clean_voice: bool = False,
    reduce_noise: bool = True,
    normalize_audio: bool = True,
    apply_filters: bool = True,
    trim_silence: bool = True,
    model_name: str = "tts_models/multilingual/multi-dataset/your_tts",
    language: str = "en"
) -> str:
    """
    Convert PDF to speech using voice cloning with Coqui TTS..
    
    Args:
        pdf_path (str): Path to PDF file
        reference_voice_path (str): Path to reference voice sample
        output_path (str): Path for output audio file
        page_range (tuple, optional): (start_page, end_page) to convert specific pages
        clean_voice (bool): Clean reference voice sample before cloning
        reduce_noise (bool): Apply noise reduction (if clean_voice=True)
        normalize_audio (bool): Normalize audio levels (if clean_voice=True)
        apply_filters (bool): Apply frequency filters (if clean_voice=True)
        trim_silence (bool): Trim silence (if clean_voice=True)
        model_name (str): TTS model to use
        language (str): Language code
    
    Returns:
        str: Path to generated audio file
    
    Raises:
        Exception: If conversion fails
    """
    if TTS is None:
        raise Exception("TTS not available. Install with: pip install TTS")
    
    try:
        print(f"📖 Extracting text from PDF: {pdf_path}")
        pages_text = extract_text_from_pdf(pdf_path, page_range)
        
        if not pages_text:
            raise Exception("No text found in PDF")
        
        # Combine all pages text
        full_text = "\n\n".join(pages_text)
        
        # Clean voice sample if requested
        voice_sample_path = reference_voice_path
        if clean_voice:
            print(f"🧹 Cleaning reference voice sample...")
            voice_sample_path = clean_voice_sample(
                reference_voice_path,
                output_path=None,  # Auto-generate cleaned filename
                reduce_noise=reduce_noise,
                normalize_audio=normalize_audio,
                apply_filters=apply_filters,
                trim_silence=trim_silence
            )
        
        print(f"🤖 Loading TTS model: {model_name}")
        
        # Initialize TTS model
        tts = TTS(model_name, progress_bar=True, gpu=False)
        
        print(f"🎙️ Converting to speech with voice cloning")
        print(f"   Text length: {len(full_text)} characters")
        print(f"   Reference voice: {voice_sample_path}")
        
        # Generate speech with voice cloning
        tts.tts_to_file(
            text=full_text,
            speaker_wav=voice_sample_path,
            language=language,
            file_path=output_path
        )
        
        print(f"✅ Cloned speech generated: {output_path}")
        return output_path
        
    except Exception as e:
        raise Exception(f"Error in PDF to speech conversion (voice cloning): {str(e)}")


def get_pdf_info(pdf_path: str) -> dict:
    """
    Get information about a PDF file.
    
    Args:
        pdf_path (str): Path to PDF file
    
    Returns:
        dict: PDF information including page count, title, etc.
    """
    try:
        doc = fitz.open(pdf_path)
        info = {
            "page_count": len(doc),
            "title": doc.metadata.get("title", "Unknown"),
            "author": doc.metadata.get("author", "Unknown"),
            "subject": doc.metadata.get("subject", ""),
            "creator": doc.metadata.get("creator", ""),
        }
        doc.close()
        return info
    except Exception as e:
        return {"error": str(e)}


# Streamlit-ready wrapper functions
def streamlit_pdf_to_speech_gtts(pdf_file, language='en', page_start=None, page_end=None, slow=False):
    """Streamlit wrapper for gTTS conversion."""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
        tmp_pdf.write(pdf_file.read())
        tmp_pdf_path = tmp_pdf.name
    
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_audio:
        tmp_audio_path = tmp_audio.name
    
    try:
        page_range = None
        if page_start is not None and page_end is not None:
            page_range = (page_start - 1, page_end - 1)  # Convert to 0-based indexing
        
        result_path = convert_pdf_to_speech_gtts(
            tmp_pdf_path, tmp_audio_path, language, page_range, slow
        )
        
        # Read audio file for return
        with open(result_path, 'rb') as f:
            audio_data = f.read()
        
        return audio_data, result_path
        
    finally:
        # Cleanup
        try:
            os.unlink(tmp_pdf_path)
        except:
            pass


def streamlit_pdf_to_speech_clone(pdf_file, voice_file, language='en', page_start=None, page_end=None, clean_voice=False, reduce_noise=True, normalize_audio=True, apply_filters=True, trim_silence=True):
    """Streamlit wrapper for voice cloning conversion."""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
        tmp_pdf.write(pdf_file.read())
        tmp_pdf_path = tmp_pdf.name
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_voice:
        tmp_voice.write(voice_file.read())
        tmp_voice_path = tmp_voice.name
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_audio:
        tmp_audio_path = tmp_audio.name
    
    try:
        page_range = None
        if page_start is not None and page_end is not None:
            page_range = (page_start - 1, page_end - 1)  # Convert to 0-based indexing
        
        result_path = convert_pdf_to_speech_voice_clone(
            tmp_pdf_path, tmp_voice_path, tmp_audio_path, page_range, clean_voice, 
            reduce_noise, normalize_audio, apply_filters, trim_silence, language=language
        )
        
        # Read audio file for return
        with open(result_path, 'rb') as f:
            audio_data = f.read()
        
        return audio_data, result_path
        
    finally:
        # Cleanup
        try:
            os.unlink(tmp_pdf_path)
            os.unlink(tmp_voice_path)
        except:
            pass


# Example usage and testing functions
def test_functions():
    """Test the functions with sample data."""
    print("🧪 Testing PDF to Speech functions...")
    
    # Test PDF info
    pdf_path = "life_3_0.pdf"
    if os.path.exists(pdf_path):
        info = get_pdf_info(pdf_path)
        print(f"PDF Info: {info}")
    
    # Test gTTS conversion
    try:
        if os.path.exists(pdf_path):
            output_gtts = convert_pdf_to_speech_gtts(
                pdf_path, "test_gtts_output.mp3", page_range=(0, 0)
            )
            print(f"gTTS test completed: {output_gtts}")
    except Exception as e:
        print(f"gTTS test failed: {e}")
    
    # Test voice cloning
    try:
        voice_path = "Waleed.wav"
        if os.path.exists(pdf_path) and os.path.exists(voice_path):
            output_clone = convert_pdf_to_speech_voice_clone(
                pdf_path, voice_path, "test_clone_output.wav", 
                page_range=(0, 0), clean_voice=True
            )
            print(f"Voice cloning test completed: {output_clone}")
    except Exception as e:
        print(f"Voice cloning test failed: {e}")


if __name__ == "__main__":
    # Run tests if script is executed directly
    test_functions()
