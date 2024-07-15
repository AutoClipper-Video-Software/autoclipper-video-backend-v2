from Types.types import ClipTimestamp
import captacity
import random
from scripts.video_editor import (
    create_clip_from_video,
    save_clip_as_video,
)
from scripts.video_downloader import download_youtube_video
from moviepy.editor import VideoFileClip

video_url = "https://youtu.be/yQ4ZIwM1-Fg"  # should come from the app's front-end
video_path = download_youtube_video(video_url)

# should come from the AI part of the back-end
clips_timestamps: list[ClipTimestamp] = [
    (32.746, 44.87),
    (46.03, 62.447),
]

clips: list[VideoFileClip] = []

for timestamp in clips_timestamps:
    clip_start = timestamp[0]
    clip_end = timestamp[1]

    clip = create_clip_from_video(clip_start, clip_end, video_file_path=video_path)
    clips.append(clip)

for clip in clips:
    videoclip = save_clip_as_video(clip)

    clip_id = random.randint(0, 1000)

    captacity.add_captions(
        video_file=videoclip,
        output_file=f"edited_clips/edited_clip{clip_id}.mp4",
        font="./fonts/Poppins-Bold.ttf",
        shadow_strength=0,
        shadow_blur=0,
        use_local_whisper=True,
    )
