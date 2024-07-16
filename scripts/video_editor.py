import os
import random
import moviepy.editor as mpy
from moviepy.editor import VideoFileClip


def create_clip_from_video(
    clip_start: float, clip_end: float, video_file_path: str
) -> VideoFileClip:
    """Simply generates a clip of a section of a given video using MoviePy.
    \n
    Returns the generated clip as a `VideoFileClip`."""

    clip: mpy.VideoFileClip = mpy.VideoFileClip(video_file_path).subclip(
        clip_start, clip_end
    )

    return clip


def save_clip_as_video(clip: mpy.VideoClip) -> str:
    """Writes the clip as a mp4 video to a folder called "clips". Creates the folder if it does not exist.
    \n
    Returns the path to the saved video."""

    clips_folder = "clips"

    if not os.path.exists(clips_folder):
        os.makedirs(clips_folder)

    clip_id = random.randint(0, 1000)

    clip_file_name = f"clip{clip_id}.mp4"

    clip_path = os.path.join(clips_folder, clip_file_name)

    clip.write_videofile(filename=clip_path, codec="libx264")

    return clip_path
