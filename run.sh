#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <text file>"
    exit 1
fi

# Assign the first argument to a variable
TEXT_FILE=$1

# Check if ffmpeg is installed and aliased
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg could not be found"
    exit 1
fi

# Check if ffprobe is installed and aliased
if ! command -v ffprobe &> /dev/null; then
    echo "ffprobe could not be found"
    exit 1
fi

# Check if required Python packages are installed
check_python_package() {
    PACKAGE=$1
    python3 -c "import $PACKAGE" &> /dev/null
    if [ $? -ne 0 ]; then
        echo "Python package $PACKAGE is not installed"
        exit 1
    fi
}
check_python_package pandas
check_python_package torch
check_python_package ray
check_python_package whisper
check_python_package yt_dlp

# Run the Python script with the provided text file
python3 arniescriber.py "$TEXT_FILE"