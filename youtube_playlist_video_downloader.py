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
                    video_urls.append(video['url'])
        return video_urls

def download_video(url):
    """Downloads the video of a given YouTube video URL with limited resolution."""
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best',  # Limit video resolution to 720p
        'merge_output_format': 'mp4',  # Merge video and audio into an MP4 file
        'ffmpeg_location': 'C:/ffmpeg/bin/ffmpeg.exe',  # Provide the path to ffmpeg
        'outtmpl': '%(title)s.%(ext)s',  # Name the file after the title of the video
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main(playlist_url):
    # Step 1: Get all video URLs in the playlist
    video_urls = get_playlist_links(playlist_url)
    
    # Step 2: Download video for each video
    print(f"Found {len(video_urls)} videos in the playlist.")
    for i, video_url in enumerate(video_urls, start=1):
        print(f"Downloading video {i}/{len(video_urls)}: {video_url}")
        try:
            download_video(video_url)
        except Exception as e:
            print(f"Failed to download video for {video_url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download videos from a YouTube playlist with limited resolution.')
    parser.add_argument('url', type=str, help='The URL of the YouTube playlist.')
    args = parser.parse_args()

    main(args.url)
