from pytubefix import YouTube
import random
from dataclasses import dataclass


class Downloader:
    """`lower_limit` and `higher_limit` are parameters that will be passed, respectively, to `random.randint()`.
    This will generate a random ID for the downloaded files."""

    def __init__(self, video_url: str, lower_limit: int, higher_limit: int):
        self.video_url = video_url
        self.lower_limit = lower_limit
        self.higher_limit = higher_limit
        self.random_file_id = random.randint(lower_limit, higher_limit)

    def download_youtube_video(self) -> str:
        """Downloads the video from YouTube using `pytube` package.
        Returns the path to the video file"""

        yt_video = YouTube(self.video_url)

        video_file_name = f"video{self.random_file_id}.mp4"

        streams = yt_video.streams

        high_resolution_stream = streams.filter().order_by("resolution").last()

        video_path = high_resolution_stream.download(
            filename=video_file_name, output_path="videos"
        )

        return video_path

    def download_audio_from_youtube_video(self) -> str:
        """Downloads the audio of a YouTube video using `pytube`.
        Returns the path to the .mp3 audio file."""

        yt_audio = YouTube(self.video_url)

        audio_file_name = f"audio{self.random_file_id}.mp3"

        audio_stream = yt_audio.streams.filter(only_audio=True).get_audio_only()

        audio_path = audio_stream.download(
            filename=audio_file_name, output_path="audios"
        )

        return audio_path
