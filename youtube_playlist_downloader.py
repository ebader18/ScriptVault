import argparse
from pytubefix import Playlist
from pytubefix.cli import on_progress


def main(playlist_url):
    pl = Playlist(playlist_url)

    print(f'Found {len(pl.videos)} videos.')
    for video in pl.videos:
        ys = video.streams.get_highest_resolution()
        ys.download()
        print(f'  Downloaded: {video.title}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download videos from a YouTube playlist.')
    parser.add_argument('url', type=str, help='The URL of the YouTube playlist to download.')
    args = parser.parse_args()

    main(args.url)
