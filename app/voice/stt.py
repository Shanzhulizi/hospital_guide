from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
import wave
import io
import json

vosk_model_path = "../models/vosk-model-small-cn-0.22"
vosk_model = Model(vosk_model_path)

async def transcribe_audio(file):
    # 将上传的文件转换为标准 WAV 格式（内存中）
    audio = AudioSegment.from_file(file.file)
    audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)

    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    wf = wave.open(wav_io, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())

    result_text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result_text += res.get("text", "")

    res = json.loads(rec.FinalResult())
    result_text += res.get("text", "")
    return result_text if result_text else "未识别到语音内容"
