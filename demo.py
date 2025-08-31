"""
Demo Script for Assignment 1 Functions
=====================================

This script demonstrates both PDF to Speech functionalities:
1. Simple conversion using gTTS
2. Voice cloning using Coqui TTS
"""

import os
import time
from Assignment1 import (
    convert_pdf_to_speech_gtts,
    convert_pdf_to_speech_voice_clone,
    clean_voice_sample,
    get_pdf_info
)

def demo_gtts_conversion():
    """Demo gTTS PDF to speech conversion."""
    print("\n" + "="*50)
    print("🔊 DEMO: PDF to Speech using gTTS")
    print("="*50)
    
    pdf_path = "life_3_0.pdf"
    output_path = "demo_gtts_output.mp3"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    try:
        # Show PDF info
        print("📖 PDF Information:")
        info = get_pdf_info(pdf_path)
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # Convert a small section
        print(f"\n🎙️ Converting page 11 to speech...")
        start_time = time.time()
        
        result = convert_pdf_to_speech_gtts(
            pdf_path=pdf_path,
            output_path=output_path,
            language='en',
            page_range=(10, 10)  # Page 11 (0-indexed)
        )
        
        end_time = time.time()
        print(f"✅ Conversion completed in {end_time - start_time:.2f} seconds")
        print(f"📄 Output saved to: {result}")
        
        if os.path.exists(result):
            file_size = os.path.getsize(result) / 1024  # KB
            print(f"📊 File size: {file_size:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_voice_cloning():
    """Demo voice cloning PDF to speech conversion."""
    print("\n" + "="*50)
    print("🎭 DEMO: PDF to Speech using Voice Cloning")
    print("="*50)
    
    pdf_path = "life_3_0.pdf"
    voice_path = "Waleed.wav"
    output_path = "demo_clone_output.wav"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    if not os.path.exists(voice_path):
        print(f"❌ Voice sample not found: {voice_path}")
        return
    
    try:
        print("🎤 Voice sample found, proceeding with cloning...")
        
        # Convert a small section with voice cloning
        print(f"🤖 Loading AI models and converting page 11...")
        start_time = time.time()
        
        result = convert_pdf_to_speech_voice_clone(
            pdf_path=pdf_path,
            reference_voice_path=voice_path,
            output_path=output_path,
            page_range=(10, 10),  # Page 11 (0-indexed)
            clean_voice=True
        )
        
        end_time = time.time()
        print(f"✅ Voice cloning completed in {end_time - start_time:.2f} seconds")
        print(f"📄 Output saved to: {result}")
        
        if os.path.exists(result):
            file_size = os.path.getsize(result) / 1024  # KB
            print(f"📊 File size: {file_size:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Note: Voice cloning requires more dependencies and processing time")

def demo_voice_cleaning():
    """Demo voice sample cleaning functionality."""
    print("\n" + "="*50)
    print("🧹 DEMO: Voice Sample Cleaning")
    print("="*50)
    
    voice_path = "Waleed.wav"
    
    if not os.path.exists(voice_path):
        print(f"❌ Voice sample not found: {voice_path}")
        return
    
    try:
        print(f"🎤 Cleaning voice sample: {voice_path}")
        
        cleaned_path = clean_voice_sample(
            voice_path=voice_path,
            output_path="demo_cleaned_voice.wav",
            reduce_noise=True,
            normalize_audio=True,
            apply_filters=True
        )
        
        print(f"✅ Voice cleaning completed")
        print(f"📄 Cleaned voice saved to: {cleaned_path}")
        
        # Compare file sizes
        if os.path.exists(voice_path) and os.path.exists(cleaned_path):
            original_size = os.path.getsize(voice_path) / 1024
            cleaned_size = os.path.getsize(cleaned_path) / 1024
            print(f"📊 Original size: {original_size:.1f} KB")
            print(f"📊 Cleaned size: {cleaned_size:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all demos."""
    print("🚀 Assignment 1 - PDF to Speech Demo")
    print("=" * 60)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    
    try:
        import gtts
        print("✅ gTTS available")
    except ImportError:
        print("❌ gTTS not available - install with: pip install gtts")
    
    try:
        import TTS
        print("✅ Coqui TTS available")
    except ImportError:
        print("❌ Coqui TTS not available - install with: pip install TTS")
    
    try:
        import noisereduce
        print("✅ Noise reduction available")
    except ImportError:
        print("⚠️ Noise reduction not available - install with: pip install noisereduce")
    
    # Run demos
    demo_gtts_conversion()
    demo_voice_cleaning()
    demo_voice_cloning()
    
    print("\n" + "="*60)
    print("🎉 Demo completed!")
    print("\nTo run the Streamlit app:")
    print("streamlit run streamlit_app.py")
    print("\nOr run individual functions from Assignment1.py")

if __name__ == "__main__":
    main()
