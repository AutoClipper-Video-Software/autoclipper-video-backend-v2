import os
from moviepy.editor import VideoFileClip
import captacity
import subprocess
import random
from pathlib import Path


def create_clip_from_video(
    clip_start: float, clip_end: float, video_path: Path
) -> VideoFileClip:
    """Simply generates a clip of a section of a given video using MoviePy.
    Returns the generated clip."""

    clip: VideoFileClip = VideoFileClip(video_path).subclip(clip_start, clip_end)

    return clip


def create_video_from_clip(clip: VideoFileClip) -> str:
    """Writes the clip as a mp4 video to a folder called "clips".
    Creates the folder if it does not exist.
    Returns the path to the created mp4 file."""

    clips_folder = "clips"

    if not os.path.exists(clips_folder):
        os.makedirs(clips_folder)

    clip_id = random.randint(0, 10000)

    clip_file_name = f"clip{clip_id}.mp4"

    clip_path = os.path.join(clips_folder, clip_file_name)

    clip.write_videofile(filename=clip_path, codec="libx264")

    return clip_path


def merge_video_and_audio(video_file: Path, audio_file: Path) -> str:
    """Simply uses ffmpeg to merge given audio and video files.
    Returns the path to the video with audio."""

    videos_with_sound_folder = "videos_with_sound"
    if not os.path.exists(videos_with_sound_folder):
        os.makedirs(videos_with_sound_folder)

    random_file_id = random.randint(0, 10000)
    output_video_name = f"video{random_file_id}.mp4"

    output_video_path = os.path.join(videos_with_sound_folder, output_video_name)

    #  ffmpeg -i video.mkv -i tamil.wav -c copy -map 0:v:0 -map 1:a:0 output.mkv
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            video_file,
            "-i",
            audio_file,
            "-c",
            "copy",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            output_video_path,
        ]
    )

    return output_video_path


def resize_clip(clip: VideoFileClip) -> VideoFileClip:
    # This is ChatGPT code.
    """Resizes the given clip to a "shorts" clip using `moviepy`.
    Returns the resized `VideoFileClip`."""

    target_aspect_ratio = 9 / 16

    # Get the current dimensions
    width, height = clip.size
    current_aspect_ratio = width / height

    if current_aspect_ratio > target_aspect_ratio:
        # The video is too wide, we need to crop the width
        new_width = int(height * target_aspect_ratio)
        crop_width = (width - new_width) // 2
        resized_clip = clip.crop(x1=crop_width, x2=width - crop_width)
    else:
        # The video is too tall, we need to crop the height
        new_height = int(width / target_aspect_ratio)
        crop_height = (height - new_height) // 2
        clip = clip.crop(y1=crop_height, y2=height - crop_height)

        target_width = 1080  # You can adjust this as needed
        target_height = int(target_width / target_aspect_ratio)
        resized_clip = clip.resize(newsize=(target_width, target_height))

    return resized_clip


def add_captions_to_clip(clip_path: Path) -> str:
    """Adds captions to the videoclip automatically using `captacity`.
    Returns the path to the edited videoclip."""

    clip_id = random.randint(0, 10000)

    if not os.path.exists("edited_clips"):
        os.makedirs("edited_clips")

    output_clip_path = f"edited_clips/edited_clip{clip_id}.mp4"

    captacity.add_captions(
        video_file=clip_path,
        output_file=output_clip_path,
        font="./fonts/Poppins-Bold.ttf",
        shadow_strength=0,
        shadow_blur=0,
        use_local_whisper=True,
        font_color="white",
        word_highlight_color="#48f542",  # green
        font_size=60,
        stroke_width=3,
    )

    return output_clip_path
