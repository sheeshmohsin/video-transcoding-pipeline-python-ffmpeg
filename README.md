# Video Transcoding Pipeline with Python and FFmpeg

This repository provides a flexible and efficient **video transcoding pipeline** implemented in **Python** using **FFmpeg**. The pipeline supports multiple transcoding formats, including **Apple HLS**, **MPEG-DASH**, and **CMAF**, and allows for parallel processing with multi-core CPU utilization.

## Features

- **Multi-format Support**: Transcode video into Apple HLS, MPEG-DASH, and CMAF formats.
- **Parallel Processing**: Optimize CPU usage by using `(available CPU cores - 2)` to balance performance and system responsiveness.
- **Flexible Pipeline**: Choose specific formats to generate or run all formats in parallel.
- **Organized Output Structure**: Outputs are organized by input file name, with separate folders for each format.

## Directory Structure

The project is organized as follows:

```
video-transcoding-pipeline-python-ffmpeg/
├── transcoder.py                # Main script to handle transcoding pipeline
├── utils.py                     # Helper functions for FFmpeg commands and core handling
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
└── output/                      # Directory for storing transcoded outputs
```

After running the transcoding pipeline, your output directory will be structured like this:

```
output/
└── input_filename/
    ├── hls/
    │   └── hls_output.m3u8 (and HLS segments)
    ├── mpeg-dash/
    │   └── dash_output.mpd (and DASH segments)
    └── cmaf/
        └── cmaf_output.mpd (and CMAF segments)
```

## Requirements

1. **FFmpeg**: Ensure FFmpeg is installed on your system.
2. **Python Libraries**: Install Python dependencies using `requirements.txt`.

### Installing FFmpeg

- **macOS**:
  ```bash
  brew install ffmpeg
  ```

- **Ubuntu**:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **Windows**:
  Download FFmpeg from [FFmpeg's official website](https://ffmpeg.org/download.html) and add it to your system's PATH.

### Installing Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Transcoding Pipeline

Run the following command, specifying the input file, output directory, and desired formats.

```bash
python transcoder.py <input_file> <output_dir> --formats hls dash cmaf
```

### Examples

1. **Generate All Formats**:

   ```bash
   python transcoder.py input_video.mp4 output --formats hls dash cmaf
   ```

2. **Generate Specific Formats** (e.g., only HLS and MPEG-DASH):

   ```bash
   python transcoder.py input_video.mp4 output --formats hls dash
   ```

3. **Default to All Formats** (if `--formats` is omitted):

   ```bash
   python transcoder.py input_video.mp4 output
   ```

## Playing the Transcoded Files

### 1. Playing HLS Content

To play the HLS output, use the `.m3u8` playlist with FFplay:

```bash
ffplay output/input_video/hls/hls_output.m3u8
```

### 2. Playing MPEG-DASH Content

Since FFplay doesn’t directly support `.mpd`, use FFmpeg to repackage the MPEG-DASH `.mpd` file into a compatible format and pipe it to FFplay:

```bash
ffmpeg -i output/input_video/mpeg-dash/dash_output.mpd -c copy -f matroska - | ffplay -
```

Alternatively, use VLC or MP4Client:

- **VLC**: Open `dash_output.mpd` in VLC via **Media > Open Network Stream**.
- **MP4Client** (from GPAC): Install GPAC and run:
  ```bash
  MP4Client output/input_video/mpeg-dash/dash_output.mpd
  ```

### 3. Playing CMAF Content

CMAF playback is similar to MPEG-DASH. Use FFmpeg to repackage the `.mpd` file for FFplay:

```bash
ffmpeg -i output/input_video/cmaf/cmaf_output.mpd -c copy -f matroska - | ffplay -
```

Or, use VLC or MP4Client to play directly from the `.mpd` manifest.

## Explanation of Key Components

1. **`transcoder.py`**: The main script that manages the transcoding process. It uses `argparse` for flexible command-line arguments to specify the input file, output directory, and formats to generate.
2. **`utils.py`**: Utility functions for managing FFmpeg commands, CPU core handling, and creating the output structure.
3. **Parallel Processing**: The pipeline utilizes `(available CPU cores - 2)` for efficient transcoding without overwhelming the system.

## License

This project is licensed under the MIT License.
