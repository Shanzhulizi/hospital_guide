from gtts import gTTS
from fastapi.responses import StreamingResponse
from io import BytesIO

def stream_text_to_speech(text: str):
    tts = gTTS(text, lang='zh')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return StreamingResponse(mp3_fp, media_type="audio/mpeg")