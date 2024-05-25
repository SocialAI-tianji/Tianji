
"""
Usage examples:

First you should download lux from https://github.com/iawia002/lux/releases

1. Download a single URL:
   python lux_downloader.py --url https://example.com/video.mp4 --output_dir /path/to/download --output_filename video.mp4 --lux_path /path/to/lux

2. Download an entire playlist from a single URL:
   python lux_downloader.py --url https://example.com/playlist --output_dir /path/to/download --lux_path /path/to/lux --playlist

3. Download multiple URLs listed in a CSV file:
   python lux_downloader.py --csv /path/to/urls.csv --output_dir /path/to/download --lux_path /path/to/lux

CSV file format (urls.csv):
URL,Title,View Count
http://www.example.com/video1,Title of Video 1,1000
http://www.example.com/video2,Title of Video 2,2000
"""
import argparse
import csv
import subprocess
import os
from typing import Optional

def download_file(url: str, output_dir: Optional[str], output_filename: Optional[str], lux_path: str, playlist: bool, title: Optional[str] = None) -> None:
    """
    Downloads a file from the specified URL using the lux executable.

    Parameters:
    url (str): The URL of the file or playlist to download.
    output_dir (Optional[str]): The directory to save the downloaded file(s).
    output_filename (Optional[str]): The name of the downloaded file. If not provided, default name from the URL will be used.
    lux_path (str): The path to the lux executable.
    playlist (bool): Whether to download an entire playlist.
    title (Optional[str]): The title of the file or playlist.
    """
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    command = [lux_path]
    
    if playlist:
        command.append('-p')

    if output_dir:
        command.extend(['-o', output_dir])
        
    if output_filename:
        command.extend(['-O', output_filename])
    
    command.append(url)

    print("Executing command:", " ".join(command))
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_lines = []

    for line in process.stdout:
        print(line, end='')
        output_lines.append(line)
    
    for line in process.stderr:
        print(line, end='')
        output_lines.append(line)
    
    process.wait()

    output_text = ''.join(output_lines)
    if process.returncode == 0 and "100.00%" in output_text:
        print("Download successful")
    else:
        error_info = " ".join(output_lines[-2:]).strip() if len(output_lines) >= 2 else "Unknown error"
        print(f"Error occurred: {error_info}")
        log_error(output_dir, url, title, error_info)

def log_error(output_dir: str, url: str, title: Optional[str], error_info: str) -> None:
    """
    Logs the error URL, title, and error info to a log file in the output directory.

    Parameters:
    output_dir (str): The directory to save the log file.
    url (str): The URL that caused the error.
    title (Optional[str]): The title of the file or playlist.
    error_info (str): The error information from the lux command.
    """
    log_file = os.path.join(output_dir, 'error_log.txt')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"URL:{url} ## Title:{title if title else 'N/A'} ## Error Info:{error_info}\n")

def download_from_csv(csv_file: str, output_dir: str, lux_path: str, playlist: bool) -> None:
    """
    Downloads files from URLs listed in a CSV file using the lux executable.

    Parameters:
    csv_file (str): The path to the CSV file containing URLs to download.
    output_dir (str): The directory to save the downloaded files.
    lux_path (str): The path to the lux executable.
    playlist (bool): Whether to download an entire playlist.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['URL']
            title = row['Title']
            filename = title.replace(' ', '_') + '.mp4'  # Assuming video files, change extension if necessary
            download_file(url, output_dir, filename, lux_path, playlist, title)

def main() -> None:
    parser = argparse.ArgumentParser(description='Download files using lux.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, help='The URL of the file to download')
    group.add_argument('--csv', type=str, help='The CSV file containing URLs to download')
    parser.add_argument('--output_dir', '-o', type=str, help='The directory to save the downloaded file', default=os.path.abspath(os.getcwd()))
    parser.add_argument('--output_filename', '-O', type=str, help='The name of the downloaded file (only for single URL)', default=None)
    parser.add_argument('--lux_path', type=str, help='The path to the lux executable', default='lux')
    parser.add_argument('--playlist', '-p', action='store_true', help='Download an entire playlist instead of a single video')
    
    args = parser.parse_args()
    
    if args.url:
        download_file(args.url, args.output_dir, args.output_filename, args.lux_path, args.playlist)
    elif args.csv:
        download_from_csv(args.csv, args.output_dir, args.lux_path, args.playlist)
    else:
        print("Please provide either a URL or a CSV file.")

if __name__ == '__main__':
    main()
