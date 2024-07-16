# Multi-Playlist Video Scraper + Transcription Tool

This tool allows you to scrape multiple profiles/playlists from any site that yt-dlp supports and transcribe the videos using Whisper from OpenAI.

## Installation

Before you start, ensure you have the necessary permissions to execute scripts. Follow these steps to install and run the tool:

### Step 1: Make the scripts executable

`chmod +x install.sh`
`chmod +x run.sh` 

### Step 2: Install the required programs

Run the `install.sh` script to install all necessary dependencies:

`./install.sh` 

The `install.sh` script will install the following programs and Python packages:

-   **pandas**
-   **torch**
-   **ray**
-   **openai-whisper**
-   **yt-dlp**
-   **ffmpeg**
-   **ffprobe**


## Usage

Create a text file (`playlists.txt`) with the URLs of the profiles/playlists you want to scrape, one URL per line. Pass this file as an argument to the `run.sh` script.

Example of `playlists.txt` for TikTok profiles:

`roucurious`<br />
`_alexciagresko`<br />
`bdtrelilbrother`<br />
`allissonmia_coronadoo`<br />
`meekotheiggy`<br />
`jairitosolano`<br />
`hayleys.worldx`<br />
`sebasmorenooo`<br />
`elcromass`<br />
`inisikiboo`<br />
`janemukbangs`<br />
`the.spectacularspi`<br />

### Run the script:
Use the `run.sh` script to execute the tool with your playlist file:

`./run.sh playlists.txt` 

The `run.sh` script will perform the following actions:

1.  Check if the required arguments are provided.
2.  Verify if `ffmpeg` and `ffprobe` are installed and available in the system.
3.  Check for the required Python packages.
4.  Run the main Python script (`arniescriber.py`) with the provided playlist file.

### Results:
The results folder set in `config.json` will contain a csv for each profile/playlist labeled `"{profile/playlist name}-id-description-transcription.csv"`

## Config
The tool uses a `config.json` file to manage settings:

-   **cpus**: The number of CPU cores to use for parallel processing. Set this to the number of cores you want the tool to utilize.
-   **gpus**: The number of GPU units to use for accelerating tasks. This should match the number of GPUs available on your machine.
-   **whispers**: The number of concurrent Whisper transcription instances to run. Adjust this based on your system's capacity.
-   **url format**: The format string for constructing URLs to scrape. The `{}` placeholder will be replaced with the specific playlist or video identifier. Ex: `"https://www.tiktok.com/@{}"` for TikTok profiles
-   **temp**: The directory path where temporary download files will be stored. Ensure this path exists or is writable.
-   **results**: The directory path where the transcription results will be saved. Ensure this path exists or is writable.
-   **model**: The Whisper model to use for transcription. Common options include `base-en` for the English language model.

## Troubleshooting

If you encounter any issues, ensure the following:

-   You have the necessary permissions to execute the scripts.
-   All required programs and Python packages are installed correctly.
-   The URLs in your `playlists.txt` file are valid playlist/profile IDs.
