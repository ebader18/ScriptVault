import argparse
import yt_dlp

def get_playlist_links(url):
    """Extracts and returns all video URLs from the YouTube playlist."""
    ydl_opts = {
        'extract_flat': True,  # Do not download videos, just extract metadata
        'skip_download': True,  # Ensure nothing gets downloaded
        'quiet': True  # Keep output clean
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract playlist info
        playlist_info = ydl.extract_info(url, download=False)
        
        # Extract URLs of all videos in the playlist
        video_urls = []
        if 'entries' in playlist_info:
            for video in playlist_info['entries']:
                if 'url' in video:
                    #video_urls.append(f"https://www.youtube.com/watch?v={video['url']}")
                    video_urls.append(video['url'])
        return video_urls

def download_audio(url):
    """Downloads the audio of a given YouTube video URL."""
    ydl_opts = {
        'format': 'bestaudio/best',  # Select the best audio quality
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # You can change this to 'm4a' or 'wav'
            'preferredquality': '192',  # Select quality (192 kbps for mp3)
        }],
        'ffmpeg_location': 'C:/ffmpeg/bin/ffmpeg.exe',  # Provide the path to ffmpeg
        'outtmpl': '%(title)s.%(ext)s',  # Name the file after the title of the video
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main(playlist_url):
    # Step 1: Get all video URLs in the playlist
    video_urls = get_playlist_links(playlist_url)
    
    # Step 2: Download audio for each video
    print(f"Found {len(video_urls)} videos in the playlist.")
    for i, video_url in enumerate(video_urls, start=1):
        print(f"Downloading audio for video {i}/{len(video_urls)}: {video_url}")
        download_audio(video_url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download audio from all videos in a YouTube playlist.')
    parser.add_argument('url', type=str, help='The URL of the YouTube playlist.')
    args = parser.parse_args()

    main(args.url)
