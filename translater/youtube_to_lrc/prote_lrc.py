import os
import whisper
import yt_dlp
from pydub import AudioSegment
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext

def download_youtube_audio(url, output_mp3_path="song.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if os.path.exists("temp_audio.mp3"):
        os.rename("temp_audio.mp3", output_mp3_path)
        print(f"✅ MP3 saved: {output_mp3_path}")
    else:
        raise FileNotFoundError("다운로드된 MP3 파일을 찾을 수 없습니다.")

    return output_mp3_path

def convert_to_wav(audio_path):
    sound = AudioSegment.from_file(audio_path)
    wav_path = "temp.wav"
    sound.export(wav_path, format="wav")
    return wav_path

def generate_lrc_with_lyrics(audio_path, input_lyrics, lrc_output_path="song.lrc"):
    wav_path = convert_to_wav(audio_path)
    model = whisper.load_model("medium")
    result = model.transcribe(wav_path, word_timestamps=True)

    os.remove(wav_path)

    # Whisper가 인식한 단어 리스트 추출
    words = []
    for segment in result['segments']:
        if "words" in segment:
            words.extend(segment["words"])

    input_lines = [line.strip() for line in input_lyrics.strip().splitlines() if line.strip()]
    lrc_lines = []
    word_idx = 0

    for line in input_lines:
        line_words = line.split()
        if word_idx >= len(words):
            break

        start_time = words[word_idx]["start"]
        minutes = int(start_time // 60)
        seconds = int(start_time % 60)
        centisec = int((start_time - int(start_time)) * 100)
        timestamp = f"[{minutes:02d}:{seconds:02d}.{centisec:02d}]"

        lrc_lines.append(f"{timestamp} {line}")
        word_idx += len(line_words)

    with open(lrc_output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lrc_lines))
    print("✅ LRC 파일 저장 완료")

def run_process():
    url = entry.get()
    lyrics = lyrics_input.get("1.0", tk.END)

    if not url or not lyrics.strip():
        messagebox.showwarning("입력 오류", "유튜브 링크와 가사를 모두 입력해주세요.")
        return

    try:
        mp3_path = download_youtube_audio(url)
        generate_lrc_with_lyrics(mp3_path, lyrics)
        messagebox.showinfo("완료", "MP3 및 LRC 파일이 생성되었습니다!")
    except Exception as e:
        messagebox.showerror("오류", str(e))

# 🎨 GUI
root = tk.Tk()
root.title("🎵 YouTube + Lyrics → LRC Generator")
root.geometry("600x500")

tk.Label(root, text="🎧 YouTube 링크:").pack(pady=(10, 0))
entry = tk.Entry(root, width=80)
entry.pack(pady=(0, 10))

tk.Label(root, text="✍️ 가사를 입력하세요:").pack()
lyrics_input = scrolledtext.ScrolledText(root, width=70, height=15)
lyrics_input.pack(pady=(0, 10))

tk.Button(root, text="🎶 변환 시작", command=run_process).pack(pady=10)

root.mainloop()