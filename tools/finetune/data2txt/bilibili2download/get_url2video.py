"""
We recommend using the script in a Linux environment.

Usage examples:

First you should download lux from https://github.com/iawia002/lux/releases

1. Download a single URL:
   python lux_downloader.py --url https://example.com/video.mp4 --output_dir /path/to/download --output_filename video.mp4 --lux_path /path/to/lux

2. Download an entire playlist from a single URL:
   python lux_downloader.py --url https://example.com/playlist --output_dir /path/to/download --lux_path /path/to/lux --playlist

3. Download multiple URLs listed in a CSV file:
   python lux_downloader.py --csv /path/to/urls.csv --output_dir /path/to/download --lux_path /path/to/lux

4. Download multiple URLs listed in a CSV file and convert to mp3 file:
   python lux_downloader.py --csv /path/to/urls.csv --output_dir /path/to/download --lux_path /path/to/lux -c


CSV file format (urls.csv):
URL,Title,View Count
http://www.example.com/video1,Title of Video 1,1000
http://www.example.com/video2,Title of Video 2,2000
"""
import argparse
import csv
import subprocess
import os
import time
import threading
from typing import Optional


def download_file(
    url: str,
    output_dir: Optional[str],
    output_filename: Optional[str],
    lux_path: str,
    playlist: bool,
    title: Optional[str] = None,
    convert_audio: bool = False,
    timeout: int = 3600,
) -> None:
    """
    Downloads a file from the specified URL using the lux executable and optionally converts it to audio.

    Parameters:
    url (str): The URL of the file or playlist to download.
    output_dir (Optional[str]): The directory to save the downloaded file(s).
    output_filename (Optional[str]): The name of the downloaded file. If not provided, default name from the URL will be used.
    lux_path (str): The path to the lux executable.
    playlist (bool): Whether to download an entire playlist.
    title (Optional[str]): The title of the file or playlist.
    convert_audio (bool): Whether to convert the downloaded video to audio.
    timeout (int): Timeout in seconds for the download process.
    """
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    command = [lux_path]

    if playlist:
        command.append("-p")

    if output_dir:
        command.extend(["-o", output_dir])

    if output_filename:
        command.extend(["-O", output_filename])

    command.append(url)

    def execute_command():
        nonlocal process
        print("Executing command:", " ".join(command))
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        output_lines = []

        for line in process.stdout:
            print(line, end="")
            output_lines.append(line)

        for line in process.stderr:
            print(line, end="")
            output_lines.append(line)

        print("等待下载进程结束")
        process.wait()

        output_text = "".join(output_lines)
        if process.returncode == 0 and "100.00%" in output_text:
            print("Download successful")
            if convert_audio and output_filename:
                convert_to_audio(
                    os.path.join(output_dir, output_filename + ".mp4"), url
                )
        else:
            error_info = (
                " ".join(output_lines[-2:]).strip()
                if len(output_lines) >= 2
                else "Unknown error"
            )
            print(f"Error occurred: {error_info}")
            log_error(output_dir, url, title, error_info)

    process = None

    while True:
        timer = threading.Timer(timeout, lambda: process.terminate())
        try:
            timer.start()
            execute_command()
            break
        except subprocess.TimeoutExpired:
            print("Process timed out, retrying...")
        finally:
            timer.cancel()


def convert_to_audio(video_file: str, url: str) -> None:
    """
    Converts a video file to an audio file using ffmpeg and deletes the original video file.

    Parameters:
    video_file (str): The path to the video file to be converted.
    url (str): The URL that was downloaded.
    """
    audio_file = os.path.splitext(video_file)[0] + ".mp3"
    command = ["ffmpeg", "-i", video_file, "-q:a", "0", "-map", "a", audio_file]

    print("Converting to audio:", " ".join(command))
    process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if process.returncode == 0:
        print(f"Conversion successful: {audio_file}")
        try:
            os.remove(video_file)
            print(f"Original video file deleted: {video_file}")
        except OSError as e:
            print(f"Error deleting original video file: {e}")
            log_error(
                os.path.dirname(video_file), url, os.path.basename(video_file), str(e)
            )
    else:
        print(f"Conversion failed: {process.stderr}")
        log_error(
            os.path.dirname(video_file),
            url,
            os.path.basename(video_file),
            process.stderr,
        )


def log_error(output_dir: str, url: str, title: Optional[str], error_info: str) -> None:
    """
    Logs the error URL, title, and error info to a log file in the output directory.

    Parameters:
    output_dir (str): The directory to save the log file.
    url (str): The URL that caused the error.
    title (Optional[str]): The title of the file or playlist.
    error_info (str): The error information from the lux command.
    """
    log_file = os.path.join(output_dir, "error_log.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(
            f"URL: {url} ## Title: {title if title else 'N/A'} ## Error Info: {error_info}\n"
        )


def download_from_csv(
    csv_file: str,
    output_dir: str,
    lux_path: str,
    playlist: bool,
    convert_audio: bool,
    timeout: int,
) -> None:
    """
    Downloads files from URLs listed in a CSV file using the lux executable.

    Parameters:
    csv_file (str): The path to the CSV file containing URLs to download.
    output_dir (str): The directory to save the downloaded files.
    lux_path (str): The path to the lux executable.
    playlist (bool): Whether to download an entire playlist.
    convert_audio (bool): Whether to convert the downloaded video to audio.
    timeout (int): Timeout in seconds for each download process.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(csv_file, newline="", encoding="utf-8") as csvfile:
        print("start")
        reader = csv.DictReader(csvfile)
        now_count = 0
        for row in reader:
            now_count += 1
            print(f"现在转换第{now_count}条")
            url = row["URL"]
            title = row["Title"]
            filename = (
                title.replace(" ", "_").replace("/", "_").replace("\\", "_")
            )  # Assuming video files, change extension if necessary
            if os.path.exists(
                os.path.join(output_dir, filename + ".mp3")
            ) or os.path.exists(os.path.join(output_dir, filename + ".mp4")):
                print(f"已存在该文件{filename}，跳过！")
                continue
            time.sleep(2)
            download_file(
                url,
                output_dir,
                filename,
                lux_path,
                playlist,
                title,
                convert_audio,
                timeout,
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Download files using lux.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", type=str, help="The URL of the file to download")
    group.add_argument(
        "--csv", type=str, help="The CSV file containing URLs to download"
    )
    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        help="The directory to save the downloaded file",
        default=os.path.abspath(os.getcwd()),
    )
    parser.add_argument(
        "--output_filename",
        "-O",
        type=str,
        help="The name of the downloaded file (only for single URL)",
        default=None,
    )
    parser.add_argument(
        "--lux_path", type=str, help="The path to the lux executable", default="lux"
    )
    parser.add_argument(
        "--playlist",
        "-p",
        action="store_true",
        help="Download an entire playlist instead of a single video",
    )
    parser.add_argument(
        "--convert_audio",
        "-c",
        action="store_true",
        help="Convert the downloaded video to audio",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        help="Timeout in seconds for the download process",
        default=6000,
    )

    args = parser.parse_args()

    if args.url:
        download_file(
            args.url,
            args.output_dir,
            args.output_filename,
            args.lux_path,
            args.playlist,
            convert_audio=args.convert_audio,
            timeout=args.timeout,
        )
    elif args.csv:
        download_from_csv(
            args.csv,
            args.output_dir,
            args.lux_path,
            args.playlist,
            convert_audio=args.convert_audio,
            timeout=args.timeout,
        )
    else:
        print("Please provide either a URL or a CSV file.")


if __name__ == "__main__":
    main()
