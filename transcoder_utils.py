# transcoder_utils.py
import subprocess

def transcode_to_h265(input_file, output_file):
    """Transcode video to H.265 (HEVC) for better compression efficiency."""
    command = [
        "ffmpeg",
        "-i", input_file,
        "-c:v", "libx265",         # Use H.265 codec
        "-crf", "28",              # Set quality level (lower CRF = higher quality)
        "-c:a", "copy",            # Copy audio without re-encoding
        output_file
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print(f"H.265 output at {output_file}")
    else:
        print(f"Error: {stderr.decode()}")

# Usage:
# transcode_to_h265("input_video.mp4", "output_h265.mp4")

def transcode_to_multiple_resolutions(input_file, output_dir):
    """Transcode video to multiple resolutions for adaptive streaming."""
    resolutions = {
        "1080p": "1920x1080",
        "720p": "1280x720",
        "480p": "854x480"
    }

    for label, resolution in resolutions.items():
        output_file = f"{output_dir}/{label}.mp4"
        command = [
            "ffmpeg",
            "-i", input_file,
            "-vf", f"scale={resolution}",    # Set video resolution
            "-c:v", "libx264",               # Use H.264 codec for compatibility
            "-crf", "23",                    # Set quality level
            "-c:a", "aac",                   # Encode audio in AAC
            output_file
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print(f"{label} output at {output_file}")
        else:
            print(f"Error: {stderr.decode()}")

# Usage:
# transcode_to_multiple_resolutions("input_video.mp4", "output_directory")

def transcode_audio_to_mp3(input_file, output_file):
    """Convert audio track to MP3 format."""
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vn",                    # Ignore video stream
        "-c:a", "libmp3lame",     # Use MP3 audio codec
        "-b:a", "192k",           # Set audio bitrate
        output_file
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print(f"MP3 audio output at {output_file}")
    else:
        print(f"Error: {stderr.decode()}")

# Usage:
# transcode_audio_to_mp3("input_video.mp4", "output_audio.mp3")
