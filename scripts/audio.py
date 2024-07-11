import pytube
import random
import os
import shutil
import whisperx
import random
from moviepy.editor import VideoFileClip


def download_audio_from_youtube_url(url: str) -> str:
    """Uses Pytube to download the audio of a YouTube video.
    \n
    Returns the path to the audio file if it was downloaded successfully.
    Otherwise, raises an exception."""

    try:
        video = pytube.YouTube(url)
        audio = video.streams.filter(only_audio=True).first()

        random_file_id = random.randint(0, 1000)
        audio_file_name = f"audio{random_file_id}.mp3"

        audio_path = audio.download(filename=audio_file_name, output_path="audios")

        return os.path.abspath(audio_path)

    except Exception:
        raise


def move_audio_to_correct_folder(audio_file: str):
    """Simply moves an audio file to the "audios" folder. Creates the folder if it does not exist."""

    destination_folder = "audios"

    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

    shutil.move(audio_file, f"{destination_folder}/{audio_file}")


def get_audio_from_clip(clip: VideoFileClip) -> str:
    """Given a MoviePy clip (`VideoFileClip`), get it's audio and save it to a .mp3 file.
    Returns the path to the audio file."""

    clip_audio = clip.audio

    random_file_id = random.randint(0, 1000)
    audio_file_name = f"audio{random_file_id}.mp3"

    clip_audio.write_audiofile(audio_file_name)

    return audio_file_name


def transcribe_audio(audio_file: str, run_on_gpu: bool) -> str:
    """Uses WhisperX (https://github.com/m-bain/whisperx.git) to get the transcript of
    the audio file and and writes that to a JSON file. The path to the generated JSON file
    is returned."""

    compute_type = "int8"

    if run_on_gpu:
        compute_type = "float16"

    device = "cuda"

    # WARN: Test a more powerful model when running on production, not the "base" model
    model = whisperx.load_model("base", device=device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=16)

    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    transcription = str(
        whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            device,
            return_char_alignments=False,
        )
    )

    transcripts_folder = "transcripts"

    if not os.path.exists(transcripts_folder):
        os.makedirs(transcripts_folder)

    random_file_id = random.randint(0, 1000)
    transcript_file_name = f"transcript{random_file_id}.json"

    transcript_file_path = os.path.join(transcripts_folder, transcript_file_name)

    with open(transcript_file_path, "w") as f:
        f.write(transcription)

    return transcript_file_path
