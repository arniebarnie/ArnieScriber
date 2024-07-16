import os, shutil
from os import path
import sys

import pandas as pd
import ray
from ray.util.multiprocessing.pool import Pool
import whisper
import torch

import yt_dlp

from config import GlobalConfig

available = torch.cuda.is_available()
CONFIG = GlobalConfig()

EXTS = {
    'audio': '.m4a',
    'description': '.description'
}

YDL = {
    'format': 'm4a/bestaudio/best', 
          'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
    'ignoreerrors' : True,
    'quiet': True,
    'noprogress': True,
    'writedescription': True,
    'outtmpl': path.join(CONFIG['temp'], '%(uploader)s/%(id)s.%(ext)s')
}


def valid(fname: str) -> bool:
    """
    Check if the file has a valid extension.

    Args:
        fname (str): The name of the file.

    Returns:
        bool: True if the file is valid, False otherwise.
    """
    return fname.endswith(EXTS['audio']) or \
           fname.endswith(EXTS['description'])

def read(fname: str) -> str:
    """
    Read the contents of a file.

    Args:
        fname (str): The name of the file.

    Returns:
        str: The contents of the file, or an empty string if the file cannot be read.
    """
    try:
        with open(fname, 'r') as file:
            return file.read()
    except:
        return ''

def downloader(profile: str) -> None:
    """
    Download the audio and description files for a given profile.

    Args:
        profile (str): The profile name.

    Returns:
        None
    """
    folder = path.join(CONFIG['temp'], profile)
    if path.isdir(folder):
        return
    
    print(f'Downloading {profile}...')
    try:
        with yt_dlp.YoutubeDL(YDL) as ydl:
            ydl.download(CONFIG['url format'].format(profile))
            print(f'Downloaded {profile}\'s videos...')
    except:
        print(f'ERROR DOWNLOADING {profile}\'s videos')

# If cuda is available, set gpu space for whispers
@ray.remote(num_gpus = CONFIG['gpus'] / CONFIG['whispers'] if available else 0)
def transcribe(afile: str, model: whisper.Whisper) -> str:
    """
    Transcribe an audio file using a Whisper model.

    Args:
        afile (str): The path to the audio file.
        model (whisper.Whisper): The Whisper model.

    Returns:
        str: The transcription of the audio file.
    """
    if not path.isfile(afile):
        return
    
    print(f'Transcribing {"/".join(afile.split("/")[-2 :])}...')
    try:
        result = model.transcribe(afile, fp16 = available)
        return result['text']
    except:
        print(f'ERROR TRANSCRIBING {"/".join(afile.split("/")[-2 :])}')
        return ''


def transcriber(args: tuple[str, ray.ObjectRef]) -> None:
    """
    Transcribe audio files for a given profile.

    Args:
        args (tuple): A tuple containing the profile name and the Whisper model object reference.

    Returns:
        None
    """
    # Unpack arguments
    profile, model = args
    print(f'Running {profile}...')
    
    # Check if profile is already transcribed
    if path.isfile(path.join(CONFIG['results'], f'{profile}-id-description-transcription.csv')):
        return
    
    # Download audios
    downloader(profile)
    folder = path.join(CONFIG['temp'], profile)
    if not path.isdir(folder):
        return
    
    # Grab audio IDs
    files = pd.Series(filter(valid, os.listdir(folder)))
    ids = files.str.split('.').str[0].unique()
    
    # Create transcription dataframe and write file names for each ID
    data = pd.DataFrame(index = ids)
    data['description'] = folder + '/' + data.index + EXTS['description']
    data['transcription'] = folder + '/' + data.index + EXTS['audio']
    
    # Read description and transcribe audio files
    data['description'] = data['description'].map(read)
    data['transcription'] = data['transcription'].map(lambda x: ray.get(transcribe.remote(x, model)))
    
    # Save results to csv and delete downloaded files
    data.to_csv(os.path.join(CONFIG['results'], f'{profile}-id-description-transcription.csv'))
    shutil.rmtree(folder)
    print(f'{profile}\'s transcription complete')
    
if __name__ == '__main__':
    # Read profiles
    with open(sys.argv[1], 'r') as file:
        profiles = list(map(lambda p: p.strip(), file.read().split('\n')))
        
    # Create temp and download folders if they do not exist
    if not path.isdir(CONFIG['temp']):
        os.makedirs(CONFIG['temp'])
    if not path.isdir(CONFIG['downloads']):
        os.makedirs(CONFIG['downloads'])
    
    # Check for cuda and load models
    device = torch.device('cuda' if available else 'cpu')
    model = whisper.load_model(CONFIG['model'], device = device)
    
    # Move models to Ray
    modelref = ray.put(model)
    modelrefs = [ray.put(whisper.load_model(CONFIG['model'], device = device)) for _ in range(CONFIG['whispers'])]
    
    # Run transcriber over all profiles
    pool = Pool()
    pool.map(transcriber, [(profile, modelrefs[i % CONFIG['whispers']]) for i, profile in enumerate(profiles)])