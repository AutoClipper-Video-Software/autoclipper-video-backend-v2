from Types.types import ClipTimestamp
from scripts.video_editor import create_clip_from_video
from scripts.video_downloader import download_youtube_video
from moviepy.editor import VideoFileClip
from scripts.audio import get_audio_from_clip, move_audio_to_correct_folder, transcribe_audio
from os import listdir
from os.path import isfile, join

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
    clip_audio = get_audio_from_clip(clip)
    move_audio_to_correct_folder(clip_audio)`

audio_files = [f for f in listdir("audios") if isfile(join("audios", f))]

for audio_file in audio_files:
    audio_transcript = transcribe_audio(audio_file, run_on_gpu=False) # run_on_gpu must be True when in production
    print(audio_transcript)