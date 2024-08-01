# Multi-Profile Video Scraper + Transcription Tool

ArnieScriber allows you to scrape multiple profiles from any site that [yt-dlp](https://github.com/yt-dlp/yt-dlp) supports and transcribe the videos using [Whisper](https://github.com/openai/whisper) from OpenAI.

## Installation

Before you start, ensure you have the necessary permissions to execute scripts. Follow these steps to install and run the tool:

### Step 1: Make the scripts executable

`chmod +x install.sh`<br />
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

Create a text file (`profiles.txt`) with the name of the profiles you want to scrape, one name per line. Pass this file as an argument to the `run.sh` script.

Example of `profiles.txt` for TikTok profiles:

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
Use the `run.sh` script to execute ArnieScriber with your profiles file:

`./run.sh profiles.txt` 

The `run.sh` script will perform the following actions:

1.  Check if the required arguments are provided.
2.  Verify if `ffmpeg` and `ffprobe` are installed and available in the system.
3.  Check for the required Python packages.
4.  Run the main Python script (`arniescriber.py`) with the provided playlist file.

### Results:
The results folder set in `config.json` will contain a csv for each profile labeled `"{profile name}-id-description-transcription.csv"`

## Config
The tool uses a `config.json` file to manage settings:

-   **cpus**: The number of CPU cores to use for parallel processing. Set this to the number of cores you want the tool to utilize.
-   **gpus**: The number of GPU units to use for accelerating tasks. This should match the number of GPUs available on your machine.
-   **whispers**: The number of concurrent Whisper transcription instances to run. Adjust this based on your system's capacity.
-   **url format**: The format string for constructing URLs to scrape. The `{}` placeholder will be replaced with the specific playlist or video identifier. Ex: `"https://www.tiktok.com/@{}"` for TikTok profiles. If you are using any other types of social media, please check the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp) to see: 
    1. If it is supported by yt-dlp.
    2. If profile scraping is supported for the specific social media platform. This script is designed to scrape **profiles**, not individual videos.
    3. Once you have verified that it is supported, replace the **url format** in the config.json file to the respective url type. Ex: `"https://www.youtube.com/@{}`
-   **temp**: The directory path where temporary download files will be stored. Ensure this path exists or is writable.
-   **results**: The directory path where the transcription results will be saved. Ensure this path exists or is writable.
-   **model**: The Whisper model to use for transcription. Common options include `base-en` for the English language model.

## YoonScraper
This tool uses a similar process as arniescriber, with the only difference being that:
    
1. It reads in a CSV or Excel file that has links in the very first column
2. It is not a multiprocessed script, so it is not ideal for large amounts of links
3. The script will return either a csv file or excel file that will contain another column containing all the transcripts
4. This script will also put an error message for the transcription if something goes wrong during the process. 

### Config

The configuration for YoonScraper is contained as the `CONFIG` dictionary to manage settings:

-   **url_format**: The fromat string for constructing URLS to scrape. The `{}` placeholder will be replaced with the specific playlist, video, or profile. x: `"https://www.tiktok.com/@{}"` for TikTok profiles. If you are using any other types of social media, please check the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp) to see: 
    1. If it is supported by yt-dlp.
    2. If profile scraping is supported for the specific social media platform. This script is designed to scrape **profiles**, not individual videos.
    3. Once you have verified that it is supported, replace the **url format** in the config.json file to the respective url type. Ex: `"https://www.youtube.com/@{}`
-   **temp**: The directory path where temporary download files will be stored. Ensure this path exists or is writable.
-   **final_file_name**: The name of file storring all the results.
-   **format**: The format of the saved file.



## Troubleshooting

If you encounter any issues, ensure the following:

-   You have the necessary permissions to execute the scripts.
-   All required programs and Python packages are installed correctly.
-   The names in your `profiles.txt` file are valid profile names.
