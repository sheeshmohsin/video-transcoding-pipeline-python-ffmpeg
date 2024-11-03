# Video Transcoding and Transmuxing Pipeline with Python and FFmpeg

A comprehensive video processing pipeline built with **Python** and **FFmpeg**, supporting both **transcoding** (changing codecs, resolution adjustments) and **transmuxing** (repackaging for adaptive streaming formats like Apple HLS, MPEG-DASH, and CMAF). This pipeline enables customizable transcoding settings, optimized CPU usage with parallel processing, and organized output structures for seamless streaming and playback.

## Features

- **Multi-format Transmuxing**: Repackage videos into Apple HLS, MPEG-DASH, and CMAF formats for adaptive streaming.
- **Customizable Transcoding**: Convert between codecs, adjust resolution and bitrate, or change audio formats.
- **Parallel Processing**: Utilize multi-core processing for efficiency, reserving system resources for other tasks.
- **Organized Output**: Automatically structures output by input file and format, making it easy to manage transcoded and transmuxed files.

## Directory Structure

```
video-transcoding-transmuxing-pipeline-python-ffmpeg/
├── transcoder.py                # Main script to manage transcoding and transmuxing pipeline
├── transcoder_utils.py          # Helper functions for specific transcoding examples
├── utils.py                     # Transmuxing utility functions and helper commands
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── output/                      # Directory for storing processed outputs
```

After processing, your output directory will look like this:

```
output/
└── input_filename/
    ├── hls/                      # HLS transmuxed output
    │   └── hls_output.m3u8       # HLS playlist and segments
    ├── mpeg-dash/                # MPEG-DASH transmuxed output
    │   └── dash_output.mpd       # MPEG-DASH manifest and segments
    ├── cmaf/                     # CMAF transmuxed output
    │   └── cmaf_output.mpd       # CMAF manifest and segments
    └── transcoded/               # Transcoded output
        ├── 1080p.mp4             # Example transcoded file in 1080p
        ├── 720p.mp4              # Example transcoded file in 720p
        └── output_h265.mp4       # Example file transcoded to H.265
```

## Requirements

1. **FFmpeg**: Ensure FFmpeg is installed on your system.
2. **MP4Box (for CMAF)**: Install GPAC if using CMAF with MP4Box.
3. **Python Libraries**: Install dependencies from `requirements.txt`.

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
  Download FFmpeg from [FFmpeg's official website](https://ffmpeg.org/download.html) and add it to your PATH.

### Installing MP4Box (for CMAF)

```bash
brew install gpac  # macOS
sudo apt install gpac  # Ubuntu
```

### Installing Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Transcoding and Transmuxing Pipeline

The main script, `transcoder.py`, lets you specify the input file, output directory, and which formats to generate. You can choose from various transmuxing formats and transcoding options.

#### Example Command

```bash
python transcoder.py input_video.mp4 output --formats hls dash cmaf
```

This command generates **HLS**, **DASH**, and **CMAF** outputs in the specified output directory.

## Transmuxing Use Cases

### 1. Apple HLS

To transmux a video into the **HLS** format:

```bash
ffmpeg -i input_video.mp4 -c copy -f hls output/hls/hls_output.m3u8
```

### 2. MPEG-DASH

To transmux a video into the **MPEG-DASH** format:

```bash
ffmpeg -i input_video.mp4 -c copy -f dash output/mpeg-dash/dash_output.mpd
```

### 3. CMAF (using MP4Box)

To create **CMAF** segments with MP4Box, use:

```bash
MP4Box -dash 4000 -frag 4000 -rap -profile dashavc264:live -bs-switching no -single-file -out output/cmaf/cmaf_output.mpd input_video.mp4
```

## Transcoding Use Cases

### 1. Codec Conversion: H.264 to H.265

Convert a video from **H.264** to **H.265** for improved compression efficiency:

```python
from transcoder_utils import transcode_to_h265
transcode_to_h265("input_video.mp4", "output_h265.mp4")
```

### 2. Resolution and Bitrate Adjustment for Adaptive Streaming

Generate multiple resolutions for adaptive streaming (1080p, 720p, 480p):

```python
from transcoder_utils import transcode_to_multiple_resolutions
transcode_to_multiple_resolutions("input_video.mp4", "output_directory")
```

### 3. Audio Format Conversion: AAC to MP3

Convert audio from **AAC** to **MP3** for compatibility with different audio players:

```python
from transcoder_utils import transcode_audio_to_mp3
transcode_audio_to_mp3("input_video.mp4", "output_audio.mp3")
```

## Transcoding Functions in `transcoder_utils.py`

Here’s a breakdown of the specific transcoding functions available:

1. **`transcode_to_h265`**:
   - Converts a video to H.265 (HEVC) format.
   - Reduces file size with minimal quality loss.

2. **`transcode_to_multiple_resolutions`**:
   - Generates multiple video resolutions for adaptive streaming.
   - Useful for platforms that require multiple quality options.

3. **`transcode_audio_to_mp3`**:
   - Converts audio to MP3 format.
   - Ideal for compatibility with older audio devices and players.

## Playing the Transmuxed Files

### HLS Content

To play HLS content:

```bash
ffplay output/hls/hls_output.m3u8
```

### MPEG-DASH Content

Play MPEG-DASH content by repackaging with FFmpeg:

```bash
ffmpeg -i output/mpeg-dash/dash_output.mpd -c copy -f matroska - | ffplay -
```

Or use **VLC** or **MP4Client** (from GPAC).

### CMAF Content

For CMAF, use:

```bash
ffmpeg -i output/cmaf/cmaf_output.mpd -c copy -f matroska - | ffplay -
```

Or play directly with **VLC** or **MP4Client**.

## License

This project is licensed under the MIT License.
