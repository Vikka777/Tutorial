import os
import shutil
import threading
from pathlib import Path

#Sorting by extensions
def sort_folder(folder):
    for filename in os.listdir(folder):
        extension = filename.split('.')[-1].upper()
        if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
            shutil.move(os.path.join(folder, filename), os.path.join(folder, 'images', filename))
        elif extension in ('AVI', 'MP4', 'MOV', 'MKV'):
            shutil.move(os.path.join(folder, filename), os.path.join(folder, 'videos', filename))
        elif extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
            shutil.move(os.path.join(folder, filename), os.path.join(folder, 'documents', filename))
        elif extension in ('MP3', 'OGG', 'WAV', 'AMR'):
            shutil.move(os.path.join(folder, filename), os.path.join(folder, 'music', filename))
        elif extension in ('ZIP', 'GZ', 'TAR'):
            shutil.unpack_archive(os.path.join(folder, filename), os.path.join(folder, 'archives', filename))
            os.remove(os.path.join(folder, filename))
        else:
            shutil.move(os.path.join(folder, filename), os.path.join(folder, 'unknown', filename))

#Normalization
import re

def normalize_filename(file_path):
    file = Path(file_path)
    old_name = file.name
    new_name = re.sub(r'[^\w\.]', '_', old_name)  # Замінюємо всі символи, крім букв і цифр, на '_'
    if old_name != new_name:
        new_path = file.with_name(new_name)
        file.rename(new_path)

def process_subfolder(subfolder):
    sort_folder(subfolder)
    for item in os.listdir(subfolder):
        item_path = os.path.join(subfolder, item)
        if os.path.isdir(item_path):
            process_subfolder(item_path)

if __name__ == '__main__':
    folder_path = '/home/users/vika/Desktop-Local/Files'  # Шлях до папки
    num_threads = 4

    #Threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=process_subfolder, args=(folder_path,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print('Folder sorted successfully.')
