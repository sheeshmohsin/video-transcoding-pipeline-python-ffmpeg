# utils.py
import os
import subprocess

def available_cores():
    """Get the number of cores available for transcoding, leaving 2 for system processes."""
    total_cores = os.cpu_count()
    return max(1, total_cores - 2)  # Leave at least 1 core available

def run_ffmpeg_command(command):
    """Execute an FFmpeg command."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode()}")
    return stdout.decode(), stderr.decode()

def ffmpeg_hls(input_file, output_dir):
    """Generate HLS format."""
    hls_dir = os.path.join(output_dir, "hls")
    os.makedirs(hls_dir, exist_ok=True)
    output_path = os.path.join(hls_dir, "hls_output.m3u8")
    command = f"ffmpeg -i {input_file} -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls {output_path}"
    run_ffmpeg_command(command)
    print(f"HLS output at {hls_dir}")

def ffmpeg_mpeg_dash(input_file, output_dir):
    """Generate MPEG-DASH format."""
    dash_dir = os.path.join(output_dir, "mpeg-dash")
    os.makedirs(dash_dir, exist_ok=True)
    output_path = os.path.join(dash_dir, "dash_output.mpd")
    command = f"ffmpeg -i {input_file} -codec: copy -f dash {output_path}"
    run_ffmpeg_command(command)
    print(f"MPEG-DASH output at {dash_dir}")

def ffmpeg_cmaf(input_file, output_dir):
    """Generate CMAF format."""
    cmaf_dir = os.path.join(output_dir, "cmaf")
    os.makedirs(cmaf_dir, exist_ok=True)
    output_path = os.path.join(cmaf_dir, "cmaf_output.mpd")
    command = f"ffmpeg -i {input_file} -codec: copy -f dash -seg_duration 4 -use_template 1 -use_timeline 1 -init_seg_name 'init.mp4' -media_seg_name 'chunk_$Number$.m4s' {output_path}"
    run_ffmpeg_command(command)
    print(f"CMAF output at {cmaf_dir}")
