import pytube
import random
import os

def download_audio_from_youtube_url(url: str) -> str:
    '''Returns the audio file path if the audio was downloaded successfully.
    Otherwise, raises an exception.'''

    try:
        video = pytube.YouTube(url)
        audio = video.streams.filter(only_audio=True).first()

        random_file_id = random.randint(0, 1000)
        audio_file_name = f'audio{random_file_id}.mp3'

        audio_path = audio.download(filename=audio_file_name, output_path='audio')

        return os.path.abspath(audio_path)
    
    except Exception:
        raise