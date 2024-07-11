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
