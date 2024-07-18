from pytubefix import YouTube
import random


def download_youtube_video(video_url: str) -> str:
    """Downloads the video (without audio!) from YouTube using `pytube` package.
    Returns the path to the video file"""

    yt_video = YouTube(video_url)

    random_file_id = random.randint(0, 10000)

    video_file_name = f"video{random_file_id}.mp4"

    streams = yt_video.streams

    high_resolution_stream = streams.filter().order_by("resolution").last()

    video_path = high_resolution_stream.download(
        filename=video_file_name, output_path="videos"
    )

    return video_path


def download_audio_from_youtube_video(video_url: str) -> str:
    """Downloads the audio of a YouTube video using `pytube`.
    Returns the path to the .mp3 audio file."""

    yt_audio = YouTube(video_url)

    random_file_id = random.randint(0, 10000)

    audio_file_name = f"audio{random_file_id}.mp3"

    audio_stream = yt_audio.streams.filter(only_audio=True).get_audio_only()

    audio_path = audio_stream.download(filename=audio_file_name, output_path="audios")

    return audio_path
