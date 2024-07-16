sudo python3 -m pip install pandas
sudo python3 -m pip install torch
sudo python3 -m pip install "ray[all]"
sudo python3 -m pip install openai-whisper
sudo python3 -m pip install yt-dlp

# Verify installation
if command -v ffmpeg &> /dev/null && command -v ffprobe &> /dev/null; then
    echo "ffmpeg and ffprobe already installed."
    exit 0
fi

cd /usr/local/bin

# Create and navigate to the ffmpeg directory
sudo mkdir -p ffmpeg && cd ffmpeg

# Download the latest ffmpeg release
sudo wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

# Extract the tar file
sudo tar -xf ffmpeg-release-amd64-static.tar.xz

# Verify and update the ffmpeg version if necessary
FFMPEG_DIR=$(find . -maxdepth 1 -type d -name 'ffmpeg-*' | head -n 1)
if [ -z "$FFMPEG_DIR" ]; then
    echo "Error: Unable to find the extracted ffmpeg directory."
    exit 1
fi

# Create symbolic links to ffmpeg and ffprobe
sudo ln -sf /usr/local/bin/ffmpeg/$FFMPEG_DIR/ffmpeg /usr/bin/ffmpeg
sudo ln -sf /usr/local/bin/ffmpeg/$FFMPEG_DIR/ffprobe /usr/bin/ffprobe

# Navigate back to the original directory
cd "$ORIGINAL_DIR"

# Verify installation
if command -v ffmpeg &> /dev/null && command -v ffprobe &> /dev/null; then
    echo "ffmpeg and ffprobe installed successfully."
else
    echo "Failed to install ffmpeg and/or ffprobe."
    exit 1
fi