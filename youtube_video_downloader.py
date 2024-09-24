# Make sure to install ffmpeg (https://www.gyan.dev/ffmpeg/builds/) and add it to the path env. variable

import argparse
import yt_dlp


def format_selector(ctx):
    """ Select the best video and the best audio that won't result in an mkv.
    NOTE: This is just an example and does not handle all cases """

    # formats are already sorted worst to best
    formats = ctx.get('formats')[::-1]

    # acodec='none' means there is no audio
    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    # find compatible audio extension
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    # vcodec='none' means there is no video
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    # These are the minimum required fields for a merged format
    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        # Must be + separated list of protocols
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }


def main(url):
    ydl_opts = {'format': format_selector, }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download video from YouTube.')
    parser.add_argument('url', type=str, help='The URL of the YouTube video to download.')
    args = parser.parse_args()

    main(args.url)