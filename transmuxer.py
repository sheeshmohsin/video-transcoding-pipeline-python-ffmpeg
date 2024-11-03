# transmuxer.py
import os
import argparse
import multiprocessing
from utils import available_cores, ffmpeg_hls, ffmpeg_mpeg_dash, ffmpeg_cmaf, mp4box_cmaf

def transmux_video(input_file, output_dir, formats):
    """Transmux video based on chosen formats in parallel."""
    # Get the base name of the input file (without extension)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    # Create a specific output directory named after the input file
    specific_output_dir = os.path.join(output_dir, base_name)
    os.makedirs(specific_output_dir, exist_ok=True)

    tasks = []
    if "hls" in formats:
        tasks.append(("HLS", ffmpeg_hls, input_file, specific_output_dir))
    if "dash" in formats:
        tasks.append(("MPEG-DASH", ffmpeg_mpeg_dash, input_file, specific_output_dir))
    if "cmaf" in formats:
        tasks.append(("CMAF", mp4box_cmaf, input_file, specific_output_dir))

    # Determine the number of cores to use for parallel processing
    cores = available_cores()
    with multiprocessing.Pool(processes=cores) as pool:
        results = [pool.apply_async(task[1], args=(task[2], task[3])) for task in tasks]

        for task, result in zip(tasks, results):
            result.wait()
            print(f"{task[0]} transmuxing completed.")

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Video Transmuxing Pipeline")
    parser.add_argument("input_file", type=str, help="Path to the input video file")
    parser.add_argument("output_dir", type=str, help="Directory to save transmuxed output files")
    parser.add_argument(
        "--formats", 
        nargs="+", 
        default=["hls", "dash", "cmaf"], 
        help="List of formats to generate (options: hls, dash, cmaf). Default is all."
    )

    args = parser.parse_args()

    # Run transmuxing based on provided arguments
    transmux_video(args.input_file, args.output_dir, args.formats)
