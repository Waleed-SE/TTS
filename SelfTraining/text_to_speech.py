import fitz  # PyMuPDF
from gtts import gTTS

pdf_file_path = 'D:\\Gen AI\\TTS\\life_3_0.pdf'
doc_pages = []

doc = fitz.open(pdf_file_path)
for page in doc:
    doc_pages.append(page.get_text())

output_audio_path = "output.mp3"
tts = gTTS(text=doc_pages[11], lang='en')
tts.save(output_audio_path)
print(f"Speech saved to {output_audio_path}")