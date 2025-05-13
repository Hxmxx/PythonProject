import whisper
from pydub import AudioSegment
import os

# 1. mp3 → wav 변환
def convert_to_wav(audio_path):
    sound = AudioSegment.from_file(audio_path)
    wav_path = "temp.wav"
    sound.export(wav_path, format="wav")
    return wav_path

# 2. Whisper로 자막 + 타이밍 분석
def generate_lrc(audio_path):
    wav_path = convert_to_wav(audio_path)
    model = whisper.load_model("base")
    result = model.transcribe(wav_path)

    lrc_lines = []
    for segment in result['segments']:
        start = segment['start']
        text = segment['text'].strip()
        minutes = int(start // 60)
        seconds = int(start % 60)
        centisec = int((start - int(start)) * 100)
        timestamp = f"[{minutes:02d}:{seconds:02d}.{centisec:02d}]"
        lrc_lines.append(f"{timestamp} {text}")

    os.remove(wav_path)
    return "\n".join(lrc_lines)

# 3. 사용 예시
audio_file = "input/your_song.mp3"  # 여기에 파일 경로 입력
lrc_output = generate_lrc(audio_file)

with open("output.lrc", "w", encoding="utf-8") as f:
    f.write(lrc_output)
print("✅ output.lrc 파일 생성 완료!")