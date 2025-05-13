from pytube import YouTube
from pydub import AudioSegment
import os

def download_youtube_audio(url, output_mp3_path="output.mp3"):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    downloaded_path = stream.download(filename="temp_audio.webm")

    # webm → mp3 변환
    audio = AudioSegment.from_file(downloaded_path)
    audio.export(output_mp3_path, format="mp3")

    os.remove(downloaded_path)
    print(f"✅ MP3 저장 완료: {output_mp3_path}")
    return output_mp3_path

# 사용 예시
youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # 바꿔서 사용
download_youtube_audio(youtube_url, "outputs/song.mp3")