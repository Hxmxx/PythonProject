import os
import time
import yt_dlp
import streamlit as st
from pydub import AudioSegment
from faster_whisper import WhisperModel
from datetime import datetime

os.makedirs("logs", exist_ok=True)

def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'UnknownTitle')
        artist = info.get('artist') or info.get('uploader', 'UnknownArtist')
        filename_base = f"{title} - {artist}".replace("/", "_").replace("\\", "_")

    temp_path = "temp_audio.mp3"
    final_mp3_path = f"{filename_base}.mp3"
    if os.path.exists(temp_path):
        os.rename(temp_path, final_mp3_path)

    return final_mp3_path, filename_base

def convert_mp3_to_wav(mp3_path):
    sound = AudioSegment.from_file(mp3_path)
    wav_path = "audio.wav"
    sound.export(wav_path, format="wav")
    return wav_path

def generate_lrc(audio_path, input_lyrics, model_size):
    model = WhisperModel(model_size, compute_type="int8")  # M1에 최적
    segments, _ = model.transcribe(audio_path, word_timestamps=True)

    words = []
    for segment in segments:
        if hasattr(segment, "words"):
            words.extend(segment.words)

    lines = input_lyrics.strip().splitlines()
    lrc = ""
    word_idx = 0

    for line in lines:
        if word_idx >= len(words):
            break
        start = words[word_idx].start
        minutes = int(start // 60)
        seconds = int(start % 60)
        centisec = int((start - int(start)) * 100)
        timestamp = f"[{minutes:02d}:{seconds:02d}.{centisec:02d}]"
        lrc += f"{timestamp} {line.strip()}\n"
        word_idx += len(line.split())

    return lrc

def save_log(url, model_name):
    with open("logs/변환기록.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] 모델: {model_name} | URL: {url}\n")

# Streamlit UI
st.set_page_config(page_title="🎵 LRC 변환기", layout="centered")

st.title("🎧 유튜브 + 가사 → LRC 변환기 (faster-whisper 버전)")
st.caption("빠르고 정확하게 타임스탬프 LRC 파일을 생성합니다.")

yt_url = st.text_input("🔗 YouTube 링크")
lyrics = st.text_area("✍️ 가사 입력", height=200)
model_choice = st.selectbox("🧠 모델 선택 (속도↑ ←→ 정확도↑)", ["tiny", "base", "small", "medium", "large"], index=2)

if st.button("🎶 변환 시작"):
    if not yt_url or not lyrics.strip():
        st.warning("YouTube 링크와 가사를 모두 입력해주세요.")
    else:
        try:
            start_time = time.time()

            with st.spinner("🎵 오디오 다운로드 중..."):
                mp3_path, filename_base = download_youtube_audio(yt_url)

            with st.spinner("🌀 LRC 생성 중..."):
                wav_path = convert_mp3_to_wav(mp3_path)
                lrc_text = generate_lrc(wav_path, lyrics, model_choice)

            save_log(yt_url, model_choice)

            lrc_filename = f"{filename_base}.lrc"
            with open(lrc_filename, "w", encoding="utf-8") as f:
                f.write(lrc_text)

            with open(mp3_path, "rb") as f:
                mp3_bytes = f.read()

            st.success("✅ 변환 완료!")
            duration = time.time() - start_time
            st.info(f"⏱ 변환 소요 시간: {duration:.2f}초")

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 MP3 다운로드", data=mp3_bytes, file_name=mp3_path, mime="audio/mpeg")
            with col2:
                st.download_button("📥 LRC 다운로드", data=lrc_text, file_name=lrc_filename, mime="text/plain")

            st.code(lrc_text)

            os.remove(mp3_path)
            os.remove(wav_path)

        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")