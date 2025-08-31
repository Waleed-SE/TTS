import fitz  # PyMuPDF
from TTS.api import TTS

# Load voice cloning model
tts = TTS("tts_models/multilingual/multi-dataset/your_tts", progress_bar=True, gpu=False)

# Path to PDF and your reference voice sample
pdf_file_path = "D:\\Gen AI\\TTS\\life_3_0.pdf"
reference_voice = "D:\\Gen AI\\TTS\\iqbal.wav"
output_audio = "life3_output.wav"

doc_pages = []

# Extract text from PDF
doc = fitz.open(pdf_file_path)
for page in doc:
    doc_pages.append(page.get_text())

# Generate speech in given voice
tts.tts_to_file(
    text=doc_pages[11],
    speaker_wav=reference_voice,
    language="en",
    file_path=output_audio
)

print(f"✅ Speech cloned in given voice saved to {output_audio}")
