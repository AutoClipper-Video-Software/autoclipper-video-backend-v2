from Types.types import ClipTimestamp
from downloader import download_audio_from_youtube_video, download_youtube_video
from editor import (
    merge_video_and_audio,
    create_clip_from_video,
    resize_clip,
    create_video_from_clip,
    add_captions_to_clip,
)

video_url = "https://youtu.be/yQ4ZIwM1-Fg"  # should come from the app's front-end

video_path = download_youtube_video(video_url)
audio_path = download_audio_from_youtube_video(video_url)

video_with_audio = merge_video_and_audio(video_path, audio_path)

# should come from the AI part of the back-end
clips_timestamps: list[ClipTimestamp] = [(32.746, 44.87), (46.03, 62.447), (70, 90)]

for timestamp in clips_timestamps:
    clip_start = timestamp[0]
    clip_end = timestamp[1]

    clip = create_clip_from_video(clip_start, clip_end, video_with_audio)

    resized_clip = resize_clip(clip)

    videoclip = create_video_from_clip(resized_clip)

    add_captions_to_clip(videoclip)
