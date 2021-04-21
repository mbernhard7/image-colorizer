#!/home/milesbernhard/.virtualenvs/updater/bin/python
import wget
import os
from pathlib import Path
import subprocess
from os import remove
from sys import argv
import shutil
import filecmp
import zipfile

if os.path.exists('backend-new'):
    shutil.rmtree('backend-new')
os.mkdir('backend-new')
wget.download('https://github.com/mbernhard7/image-colorizer/archive/refs/heads/main.zip', 'main.zip')
with zipfile.ZipFile("main.zip","r") as archive:
    for file in archive.infolist():
        if file.filename.startswith('image-colorizer-main/backend/'):
            file.filename='backend-new/'+file.filename.split('backend/')[1]
            archive.extract(file)
os.remove("main.zip")
print("\nDownloaded and extracted new backend.")
for directory, subdirectories, files in os.walk('backend-new'):
    for file in files:
        new_name=os.path.join(directory, file)
        old_name=new_name.replace('backend-new/','')
        if os.path.exists(old_name):
            print('\nComparing '+old_name+' with new version.')
            if not filecmp.cmp(new_name, old_name):
                os.remove(old_name)
                os.rename(new_name,old_name)
                print("Replaced "+old_name+" with new version.\n")
if os.path.exists('backend-new'):
    shutil.rmtree('Deleted download.\n')
print(subprocess.run(['bash', 'reinstall_reqs.sh'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
print("\nReloaded virtualenv.")
Path('/var/www/milesbernhard_pythonanywhere_com_wsgi.py').touch() #triggers web app reload
print("\nReloaded app.")