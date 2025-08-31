"""
Streamlit App fo# Import our assignment functions
try:
    from Assignment1 import (
        streamlit_pdf_to_speech_gtts,
        streamlit_pdf_to_speech_clone,
        get_pdf_info,
        clean_voice_sample
    )
except ImportError:
    st.error("Please ensure Assignment1.py is in the same directory")
    st.stop()eech Conversion
==========================================

This app provides two main functionalities:
1. Simple PDF to Speech using gTTS
2. PDF to Speech with Voice Cloning using Coqui TTS

Features:
- Upload PDF files and convert specific pages
- Upload voice samples for cloning
- Optional voice cleaning and noise reduction
- Download generated audio files
"""

import streamlit as st
import tempfile
import os
from pathlib import Path
import time

# Import our assignment functions
try:
    from Assignment1 import (
        streamlit_pdf_to_speech_gtts,
        streamlit_pdf_to_speech_clone,
        get_pdf_info,
        clean_voice_sample
    )
except ImportError:
    st.error("Please ensure assignment1.py is in the same directory")
    st.stop()


def main():
    st.set_page_config(
        page_title="PDF to Speech Converter",
        page_icon="🎙️",
        layout="wide"
    )
    
    st.title("🎙️ PDF to Speech Converter")
    st.markdown("Convert PDF documents to speech using Google TTS or Voice Cloning")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    mode = st.sidebar.radio(
        "Choose Conversion Mode:",
        ["🔊 Simple TTS (gTTS)", "🎭 Voice Cloning (TTS)"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown("""
    - **Simple TTS**: Uses Google Text-to-Speech for quick conversion
    - **Voice Cloning**: Uses AI to clone a reference voice for personalized speech
    """)
    
    # Main content area
    if mode == "🔊 Simple TTS (gTTS)":
        gtts_interface()
    else:
        voice_cloning_interface()


def gtts_interface():
    """Interface for Google Text-to-Speech conversion."""
    st.header("🔊 Simple PDF to Speech (Google TTS)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload
        uploaded_pdf = st.file_uploader(
            "📄 Upload PDF file",
            type=['pdf'],
            help="Upload a PDF document to convert to speech"
        )
        
        if uploaded_pdf:
            # Show PDF info
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                tmp_file.write(uploaded_pdf.read())
                tmp_path = tmp_file.name
                uploaded_pdf.seek(0)  # Reset file pointer
            
            try:
                pdf_info = get_pdf_info(tmp_path)
                st.success(f"📖 PDF loaded: {pdf_info.get('page_count', 'Unknown')} pages")
                
                if pdf_info.get('title') != 'Unknown':
                    st.info(f"Title: {pdf_info['title']}")
                
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
                return
            finally:
                try:
                    os.unlink(tmp_path)
                except:
                    pass
    
    with col2:
        # Settings
        st.subheader("⚙️ Settings")
        
        language = st.selectbox(
            "🌐 Language",
            ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
            index=0,
            help="Select the language for text-to-speech"
        )
        
        slow_speech = st.checkbox(
            "🐌 Slow speech",
            help="Generate speech at slower pace"
        )
        
        # Page range
        st.subheader("📄 Page Range")
        use_page_range = st.checkbox("Select specific pages")
        
        page_start, page_end = None, None
        if use_page_range and uploaded_pdf:
            col_start, col_end = st.columns(2)
            with col_start:
                page_start = st.number_input("Start page", min_value=1, value=1)
            with col_end:
                page_end = st.number_input("End page", min_value=1, value=1)
    
    # Convert button
    if uploaded_pdf and st.button("🎙️ Convert to Speech", type="primary"):
        with st.spinner("Converting PDF to speech..."):
            try:
                audio_data, audio_path = streamlit_pdf_to_speech_gtts(
                    uploaded_pdf, language, page_start, page_end, slow_speech
                )
                
                st.success("✅ Conversion completed!")
                
                # Audio player
                st.audio(audio_data, format='audio/mp3')
                
                # Download button
                st.download_button(
                    label="💾 Download Audio",
                    data=audio_data,
                    file_name=f"pdf_speech_{int(time.time())}.mp3",
                    mime="audio/mp3"
                )
                
            except Exception as e:
                st.error(f"❌ Conversion failed: {str(e)}")


def voice_cloning_interface():
    """Interface for voice cloning conversion."""
    st.header("🎭 PDF to Speech with Voice Cloning")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File uploads
        uploaded_pdf = st.file_uploader(
            "📄 Upload PDF file",
            type=['pdf'],
            key="clone_pdf",
            help="Upload a PDF document to convert to speech"
        )
        
        uploaded_voice = st.file_uploader(
            "🎤 Upload Voice Sample",
            type=['wav', 'mp3', 'flac'],
            help="Upload a clear voice sample (10-30 seconds recommended)"
        )
        
        if uploaded_pdf:
            # Show PDF info
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                tmp_file.write(uploaded_pdf.read())
                tmp_path = tmp_file.name
                uploaded_pdf.seek(0)  # Reset file pointer
            
            try:
                pdf_info = get_pdf_info(tmp_path)
                st.success(f"📖 PDF loaded: {pdf_info.get('page_count', 'Unknown')} pages")
                
                if pdf_info.get('title') != 'Unknown':
                    st.info(f"Title: {pdf_info['title']}")
                
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
                return
            finally:
                try:
                    os.unlink(tmp_path)
                except:
                    pass
        
        if uploaded_voice:
            st.success("🎤 Voice sample uploaded successfully")
            
            # Play voice sample
            st.audio(uploaded_voice.read(), format='audio/wav')
            uploaded_voice.seek(0)  # Reset file pointer
    
    with col2:
        # Settings
        st.subheader("⚙️ Settings")
        
        language = st.selectbox(
            "🌐 Language",
            ["en", "es", "fr", "de", "it", "pt"],
            index=0,
            key="clone_lang",
            help="Select the language for text-to-speech"
        )
        
        # Voice cleaning options
        st.subheader("🧹 Voice Enhancement")
        clean_voice = st.checkbox(
            "✨ Enable voice cleaning",
            value=True,
            help="Remove noise and enhance voice quality"
        )
        
        # Advanced cleaning options (only shown when cleaning is enabled)
        if clean_voice:
            with st.expander("🔧 Advanced Cleaning Options", expanded=False):
                reduce_noise = st.checkbox(
                    "🔇 Noise reduction",
                    value=True,
                    help="Remove background noise using AI"
                )
                normalize_audio = st.checkbox(
                    "🎚️ Audio normalization",
                    value=True,
                    help="Adjust volume levels for consistency"
                )
                apply_filters = st.checkbox(
                    "🔊 Frequency filtering",
                    value=True,
                    help="Remove unwanted low/high frequencies"
                )
                trim_silence = st.checkbox(
                    "✂️ Silence trimming",
                    value=True,
                    help="Remove silence from beginning and end"
                )
                
                if any([reduce_noise, normalize_audio, apply_filters, trim_silence]):
                    st.success("Voice cleaning features enabled:")
                    features = []
                    if reduce_noise: features.append("🔇 Noise reduction")
                    if normalize_audio: features.append("🎚️ Audio normalization")
                    if apply_filters: features.append("🔊 Frequency filtering")
                    if trim_silence: features.append("✂️ Silence trimming")
                    st.markdown("- " + "\n- ".join(features))
        else:
            # Set default values when cleaning is disabled
            reduce_noise = False
            normalize_audio = False
            apply_filters = False
            trim_silence = False
            st.warning("⚠️ Voice cleaning disabled - may affect cloning quality")
        
        # Page range
        st.subheader("📄 Page Range")
        use_page_range = st.checkbox("Select specific pages", key="clone_pages")
        
        page_start, page_end = None, None
        if use_page_range and uploaded_pdf:
            col_start, col_end = st.columns(2)
            with col_start:
                page_start = st.number_input("Start page", min_value=1, value=1, key="clone_start")
            with col_end:
                page_end = st.number_input("End page", min_value=1, value=1, key="clone_end")
    
    # Convert button
    if uploaded_pdf and uploaded_voice and st.button("🎭 Clone Voice & Convert", type="primary"):
        with st.spinner("Converting PDF to speech with voice cloning..."):
            try:
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Loading AI models...")
                progress_bar.progress(25)
                
                status_text.text("Processing voice sample...")
                progress_bar.progress(50)
                
                status_text.text("Generating cloned speech...")
                progress_bar.progress(75)
                
                audio_data, audio_path = streamlit_pdf_to_speech_clone(
                    uploaded_pdf, uploaded_voice, language, page_start, page_end, 
                    clean_voice, reduce_noise, normalize_audio, apply_filters, trim_silence
                )
                
                progress_bar.progress(100)
                status_text.text("Conversion completed!")
                
                st.success("✅ Voice cloning completed!")
                
                # Audio player
                st.audio(audio_data, format='audio/wav')
                
                # Download button
                st.download_button(
                    label="💾 Download Cloned Audio",
                    data=audio_data,
                    file_name=f"cloned_speech_{int(time.time())}.wav",
                    mime="audio/wav"
                )
                
            except Exception as e:
                st.error(f"❌ Voice cloning failed: {str(e)}")
                st.info("💡 Try uploading a clearer voice sample or check if all dependencies are installed")


def show_requirements():
    """Show installation requirements."""
    st.sidebar.markdown("---")
    with st.sidebar.expander("📦 Installation Requirements"):
        st.code("""
# Core dependencies
pip install streamlit
pip install PyMuPDF
pip install gtts
pip install TTS
pip install librosa
pip install soundfile

# Optional (for voice cleaning)
pip install noisereduce
pip install scipy
        """, language="bash")


if __name__ == "__main__":
    show_requirements()
    main()
