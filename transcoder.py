# transcoder.py
import os
import argparse
from utils import ffmpeg_hls, ffmpeg_mpeg_dash, mp4box_cmaf
from transcoder_utils import transcode_to_h265, transcode_to_multiple_resolutions, transcode_audio_to_mp3

def transmux(input_file, output_dir, formats):
    """Handle transmuxing options for HLS, MPEG-DASH, and CMAF."""
    print("Starting transmuxing...")
    if "hls" in formats:
        ffmpeg_hls(input_file, os.path.join(output_dir, "hls"))
    if "dash" in formats:
        ffmpeg_mpeg_dash(input_file, os.path.join(output_dir, "mpeg-dash"))
    if "cmaf" in formats:
        mp4box_cmaf(input_file, os.path.join(output_dir, "cmaf"))
    print("Transmuxing completed.")

def transcode(input_file, output_dir, transcoding_tasks):
    """Handle transcoding tasks such as codec conversion and resolution adjustment."""
    print("Starting transcoding...")
    output_transcoded_dir = os.path.join(output_dir, "transcoded")
    os.makedirs(output_transcoded_dir, exist_ok=True)
    
    if "h265" in transcoding_tasks:
        output_file = os.path.join(output_transcoded_dir, "output_h265.mp4")
        transcode_to_h265(input_file, output_file)
    if "resolutions" in transcoding_tasks:
        transcode_to_multiple_resolutions(input_file, output_transcoded_dir)
    if "mp3_audio" in transcoding_tasks:
        output_file = os.path.join(output_transcoded_dir, "output_audio.mp3")
        transcode_audio_to_mp3(input_file, output_file)
    print("Transcoding completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Transcoding and Transmuxing Pipeline")
    parser.add_argument("input_file", type=str, help="Path to the input video file")
    parser.add_argument("output_dir", type=str, help="Directory to save processed output files")

    # Transmuxing options
    parser.add_argument(
        "--transmux",
        nargs="+",
        choices=["hls", "dash", "cmaf"],
        help="Specify which formats to transmux to (hls, dash, cmaf)"
    )

    # Transcoding options
    parser.add_argument(
        "--transcode",
        nargs="+",
        choices=["h265", "resolutions", "mp3_audio"],
        help="Specify transcoding tasks (h265 for codec conversion, resolutions for multiple resolutions, mp3_audio for audio conversion)"
    )

    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Run transmuxing if specified
    if args.transmux:
        transmux(args.input_file, args.output_dir, args.transmux)

    # Run transcoding if specified
    if args.transcode:
        transcode(args.input_file, args.output_dir, args.transcode)
