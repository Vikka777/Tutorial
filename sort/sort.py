import os
import shutil
from pathlib import Path #шлях

#p = Path('/home/users/vika/Desktop-Local/Files')
#функція, яка сортує папки за розширеннями
def sort_folder(folder):
    p = Path('/home/users/vika/Desktop-Local/Files')
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

#функція normilize
import re

def normalize_filename(file_path):
    file = Path(file_path)
    old_name = file.name
    new_name = re.sub(r'[^\w\.]', '_', old_name) # заменяем все символы, кроме букв и цифр, на '_'
    if old_name != new_name:
        new_path = file.with_name(new_name)
        file.rename(new_path)

    if __name__ == '__main__':
        folder_path = '/home/users/vika/Desktop-Local/Files'
        sort_folder(folder_path)
        print('Folder sorted successfully.')
