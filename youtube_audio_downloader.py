import argparse
import yt_dlp

def main(url):
    # Setting yt-dlp options for audio only
    ydl_opts = {
        'format': 'bestaudio/best',  # Select the best audio quality
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # You can change this to 'm4a' or 'wav' if you prefer another format
            'preferredquality': '192',  # Select quality (192 kbps for mp3)
        }],
        'ffmpeg_location': 'C:/ffmpeg/bin/ffmpeg.exe',  # Ensure ffmpeg is installed and in PATH
        'outtmpl': '%(title)s.%(ext)s',  # Name the file after the title of the video
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download audio from YouTube.')
    parser.add_argument('url', type=str, help='The URL of the YouTube video to download.')
    args = parser.parse_args()

    main(args.url)
