import argparse
import yt_dlp

def get_playlist_links(url):
    # yt-dlp options to extract information but not download
    ydl_opts = {
        'extract_flat': True,  # Do not download videos, just extract metadata
        'skip_download': True,  # Ensure nothing gets downloaded
        'quiet': True  # Keep output clean
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract playlist info
        playlist_info = ydl.extract_info(url, download=False)
        
        # Print the links of all videos in the playlist
        if 'entries' in playlist_info:
            for video in playlist_info['entries']:
                if 'url' in video:
                    print(f"https://www.youtube.com/watch?v={video['url']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get video URLs from a YouTube playlist.')
    parser.add_argument('url', type=str, help='The URL of the YouTube playlist.')
    args = parser.parse_args()

    get_playlist_links(args.url)
