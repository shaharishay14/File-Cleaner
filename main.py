from os import scandir, rename
import os
from os.path import splitext, exists, join
from shutil import move
import shutil
from time import sleep

import logging
import time




from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
source_folder = "/Users/shaharishay/Downloads"
dest_folder_sfx = "/Users/shaharishay/Downloads/SFX_Downloads"
dest_folder_music = "/Users/shaharishay/Downloads/Music_Downloads"
dest_folder_videos = "/Users/shaharishay/Downloads/Videos_Downloads"
dest_folder_images = "/Users/shaharishay/Downloads/Images_Downloads"
dest_folder_documents = "/Users/shaharishay/Downloads/Documents_Downloads"
dest_folder_code = "/Users/shaharishay/Downloads/Code_Downloads"
dest_folder_compressed = "/Users/shaharishay/Downloads/Compressed_Downloads"

#Images
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
#Videos
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
#Audio
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

#Documents
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv", ".xml"]

#Code
code_extensions = [".py", ".java", ".class", ".js", ".html", ".css", ".s", ".jar", ".vsix"]

#Zip
zip_extensions = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz", ".tbz2", ".txz"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    original_path = entry.path
    destination_path = join(dest, name)
    
    # Check if the file already exists at the destination
    if exists(destination_path):
        # Generate a unique name for the file
        unique_name = make_unique(dest, name)
        destination_path = join(dest, unique_name)
    
    # Move the file to the destination with the new unique name
    shutil.move(original_path, destination_path)
    logging.info(f"Moved file '{original_path}' to '{destination_path}'") 

class MoveHandler(FileSystemEventHandler):
   # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_folder"
    # ? .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with scandir(source_folder) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                    dest = dest_folder_sfx
                else:
                    dest = dest_folder_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_folder_videos, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_folder_images, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_folder_documents, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_code_files(self, entry, name):  # * Checks all Document Files
        for code_extension in code_extensions:
            if name.endswith(code_extension) or name.endswith(code_extension.upper()):
                move_file(dest_folder_code, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_zip_files(self, entry, name):  # * Checks all Document Files
        for zip_extension in zip_extensions:
            if name.endswith(zip_extension) or name.endswith(zip_extension.upper()):
                move_file(dest_folder_code, entry, name)
                logging.info(f"Moved document file: {name}")

def sort_exisiting_files():
    handler = MoveHandler()
    with scandir(source_folder) as entries:
        for entry in entries:
            if entry.is_file(): 
                name = entry.name
                handler.check_audio_files(entry, name)
                handler.check_video_files(entry, name)
                handler.check_image_files(entry, name)
                handler.check_document_files(entry, name)
                handler.check_code_files(entry, name)
                handler.check_zip_files(entry, name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    sort_exisiting_files()

    path = source_folder
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()        