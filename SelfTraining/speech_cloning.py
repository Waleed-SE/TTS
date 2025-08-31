import fitz  # PyMuPDF
from TTS.api import TTS
import whisper

input_audio = "D:\\Gen AI\\TTS\\output.mp3"  # or "input.wav"
reference_voice = "D:\\Gen AI\\TTS\\waleed.wav"
output_audio = "cloned_output.wav"

# Load voice cloning model
tts = TTS("tts_models/multilingual/multi-dataset/your_tts", progress_bar=True, gpu=False)

model = whisper.load_model("base")
result = model.transcribe(input_audio)
transcribed_text = result["text"]
print("Transcribed text:", transcribed_text)

# Generate speech in given voice
tts.tts_to_file(
    text=transcribed_text,
    speaker_wav=reference_voice,
    language="en",
    file_path=output_audio
)

print(f"✅ Speech cloned in given voice saved to {output_audio}")
