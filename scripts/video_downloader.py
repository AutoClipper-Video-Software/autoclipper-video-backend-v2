from pytube import YouTube
import random


def download_youtube_video(video_url: str) -> str:
    """Downloads the video from YouTube using `pytube` package.
    Returns the path to the video file"""

    yt_video = YouTube(video_url)

    random_file_id = random.randint(0, 1000)
    video_file_name = f"video{random_file_id}.mp4"

    video = yt_video.streams.get_highest_resolution()

    video_path = video.download(filename=video_file_name, output_path="videos")

    return video_path
