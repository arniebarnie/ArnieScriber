import pandas as pd
import os
from os import path
import yt_dlp
import whisper

#Configuration
CONFIG = {
    "url_format": "https://www.instagram.com/p/{}/?hl=en",
    "temp": "downloads",
    "model": "base.en",
    "final_file_name" : "Data",
    "format" : "xslx"
}

#Ensure the temporary download directory exists
if not path.exists(CONFIG['temp']):
    os.makedirs(CONFIG['temp'])

#yt-dlp configuration for downloading and extracting audio
YDL = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
    'ignoreerrors': True,
    'quiet': True,
    'noprogress': True,
    'outtmpl': path.join(CONFIG['temp'], '%(id)s.%(ext)s')
}

#Function to download video and return the path to the audio file
def downloader(video_url):
    try:
        video_id = video_url.split('/')[-2]
        print(f'Downloading video id {video_id}')
        
        with yt_dlp.YoutubeDL(YDL) as ydl:
            error_code = ydl.download(video_url)
        
        # Find the downloaded audio file
        audio_file_path = path.join(CONFIG['temp'], f'{video_id}.m4a')
        if path.isfile(audio_file_path):
            print(f'Audio file saved to {audio_file_path}')
            return audio_file_path
        else:
            print(f'No audio file found for video id {video_id}')
            return (None, error_code)
    
    except Exception as e:
        print(f'ERROR DOWNLOADING {video_url}: {e}')
        return None

#Function to transcribe audio file using Whisper
def transcribe(afile, model):
    if not path.isfile(afile):
        print(f'File {afile} does not exist')
        return None
    
    print(f'Transcribing {afile}')
    try:
        result = model.transcribe(afile, fp16 = False)
        return result['text']
    except Exception as exception:
        print(f"ERROR TRANSCRIBING {afile}: {exception}")
        return None

#Load the Whisper model
model = whisper.load_model(CONFIG['model'])

if __name__ == '__main__':
    #Insert filecontaining 
    filename = ""
    if filename.split('.')[-1] == 'xslx':
        df = pd.read_excel(filename)   
    elif filename.split('.')[-1] == 'csv':
        df = pd.read_csv(filename)
    else:
        raise ValueError('Invalid input file')

    #renaming the first column to link
    df.columns.values[0] = 'link'
#Process each link in the Excel file
    transcription_list = []
    for _, row in df.iterrows():
        video_url = row['link']  
        audio_file_path = downloader(video_url)
        if isinstance(audio_file_path, tuple):
            transcription_list.append(f"DOWNLOADING ERROR CODE {audio_file_path[1]}")
            continue 
        if audio_file_path:
            transcription = transcribe(audio_file_path, model)
            if transcription:
                print(f'Transcription for {video_url}:')
                transcription_list.append(transcription)
            else:
                print(f'No transcription available for {video_url}')
                transcription = "failed transcription"
                transcription_list.append(transcription)

    df['transcription'] = transcription_list
    
    if CONFIG['format'] == 'csv':
        df.to_csv(CONFIG['final_file_name'] + "." + CONFIG['format'])
        print("exported to csv file successfully")
    elif CONFIG['format'] == 'xslx':
        df.to_excel(CONFIG['final_file_name'] + "." + CONFIG['format'])
        print('exported to excel file successfully')
    else:
        raise ValueError("Invalid final file format")
