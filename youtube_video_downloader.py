import argparse
from pytubefix import YouTube
from pytubefix.cli import on_progress


def main(url):
    yt = YouTube(url, on_progress_callback=on_progress)

    ys = yt.streams.get_highest_resolution()
    ys.download()
    print('Downloaded')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download video from YouTube.')
    parser.add_argument('url', type=str, help='The URL of the YouTube video to download.')
    args = parser.parse_args()

    main(args.url)
