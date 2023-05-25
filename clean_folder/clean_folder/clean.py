import os
import shutil
import sys
import re

from pathlib import Path #шлях

#функція, яка сортує папки за розширеннями
def sort_folder(folder):
    for filename in os.listdir(folder):
        extension = filename.split('.')[-1].upper()
        if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
            if not os.path.exists(os.path.join(folder, 'images')):# треба перевіряти якщо папка не існує, то створювати
                os.mkdir(os.path.join(folder, 'images'))
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

def normalize_filename(file_path):
    file = Path(file_path)
    old_name = file.name
    new_name = re.sub(r'[^\w\.]', '_', old_name) # заменяем все символы, кроме букв и цифр, на '_'
    if old_name != new_name:
        new_path = file.with_name(new_name)
        file.rename(new_path)
if __name__ == '__main__':
    folder_path = sys.argv[1] # передача шляху до папки, яку потрібно сортувати, через аргументи командного рядка
    sort_folder(folder_path)
    print('Folder sorted successfully.')