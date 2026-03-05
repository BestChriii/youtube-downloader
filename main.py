import yt_dlp
import subprocess
import os
import config

RAW_DIR = os.path.join(config.VIDEOS_DIR, "raws")
OUT_DIR = config.VIDEOS_DIR
FFMPEG_PATH = os.getenv("FFMPEG_PATH")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


def clean_urls(urls):
    return [u.strip() for u in urls if u.strip()]


def download_videos(urls):

    urls = clean_urls(urls)

    if not urls:
        return

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"{RAW_DIR}/%(title)s.%(ext)s",
        "ffmpeg_location": FFMPEG_PATH,
        "merge_output_format": "mkv",
        "noplaylist": False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)


def convert_to_mp4():

    for file in os.listdir(RAW_DIR):

        input_path = os.path.join(RAW_DIR, file)

        if not os.path.isfile(input_path):
            continue

        name = os.path.splitext(file)[0]
        output_path = os.path.join(OUT_DIR, f"{name}.mp4")

        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            output_path
        ]

        subprocess.run(command)

        os.remove(input_path)


def main():

    try:

        if hasattr(config, "VIDEOS_URL"):
            download_videos(config.VIDEOS_URL)

        if hasattr(config, "PLAYLISTS_URL"):
            download_videos(config.PLAYLISTS_URL)

        convert_to_mp4()

        print("Download e conversione completati.")

    except Exception as e:
        print(f"Errore: {e}")


if __name__ == "__main__":
    main()