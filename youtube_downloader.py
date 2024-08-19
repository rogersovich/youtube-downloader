import yt_dlp
from tqdm import tqdm
import time
import os
import re

def format_time(seconds):
    # Format waktu dalam format yang ramah pengguna (detik, menit, jam).
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{int(minutes)} minutes and {seconds:.2f} seconds"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{int(hours)} hours, {int(minutes)} minutes and {seconds:.2f} seconds"

def download_video(url):
    # Unduh video dari URL yang diberikan dan simpan di folder yang ditentukan.
    global start_time, pbar

    try:
        # Pastikan folder hasil unduhan ada
        output_folder = '/yt_downloader_result'
        os.makedirs(output_folder, exist_ok=True)

        start_time = time.time()  # Waktu mulai unduhan
        pbar = tqdm(total=100, desc="Overall Progress", unit="%", unit_scale=True)
    
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # Pilih video dengan kualitas maksimal 1080p atau 720p dan audio terbaik
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Tentukan folder output
            'progress_hooks': [progress_hook],  # Hook untuk menangani progress unduhan
            'postprocessor_hooks': [postprocessor_hook],  # Hook untuk menangani progress post-processing (merging)
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        end_time = time.time()
        total_time = end_time - start_time
        formatted_time = format_time(total_time)
        print(f"Total elapsed time: {formatted_time}")

    except Exception as e:
        print(f"An error occurred: {e}")

def progress_hook(d):
    # Hook untuk menangani progress unduhan
    if d['status'] == 'downloading':
        pbar.update(1)  # Update progress bar secara keseluruhan
    elif d['status'] == 'finished':
        pbar.set_postfix_str("Download complete")

def postprocessor_hook(d):
    # Hook untuk menangani progress post-processing (merging)
    if d['status'] == 'processing':
        print("Merging in progress...")
    elif d['status'] == 'finished':
        print("Merging completed!")

def is_youtube_url(url):
    # Periksa apakah URL adalah URL YouTube
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+'
        r'|(https?://)?(www\.)?youtu\.be/[\w-]+', re.IGNORECASE)
    return re.match(youtube_regex, url) is not None

def download_multi_videos(file_path):
    # Baca file dengan URL dan unduh setiap video yang valid
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    for url in urls:
        url = url.strip()
        if is_youtube_url(url):
            print(f"Downloading video from: {url}")
            download_video(url)
        else:
            print(f"Bukan URL YouTube: {url}")

def main():
    # Menu untuk memilih antara unduhan single dan multi
    choice = input("Select mode:\n1. Single\n2. Multi\nEnter choice (1/2): ").strip()

    if choice == '1':
        url = input("Enter the URL of the YouTube video: ").strip()
        if is_youtube_url(url):
            download_video(url)
        else:
            print("Bukan URL YouTube")
    elif choice == '2':
        file_path = 'youtube_multi.txt'
        if os.path.exists(file_path):
            download_multi_videos(file_path)
        else:
            print(f"File {file_path} tidak ditemukan.")
    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
