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

app_changed=False
requirements_changed=False
this_changed=False
if os.path.exists('backend-new'):
    shutil.rmtree(os.path.abspath('backend-new'))
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
                app_changed=True
                if 'requirements' in new_name:
                    requirements_changed=True
                if 'update_backend' in new_name:
                    this_changed=True
            else:
                print("No changes detected.\n")
if os.path.exists('backend-new'):
    shutil.rmtree(os.path.abspath('backend-new'))
    print('Deleted download.\n')
if requirements_changed:
    print('Requirements changed.')
    print(subprocess.run(['bash', 'reinstall_reqs.sh'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    print("\nReloaded virtualenv.")
if app_changed:
    print('App changed.')
    Path('/var/www/milesbernhard_pythonanywhere_com_wsgi.py').touch() #triggers web app reload
    print("\nReloaded app.")
    if this_changed:
        print('\nUpdate script changed. Triggering re-run...')
        print(subprocess.run(['bash', 'reupdate_backend.sh', str(os.getpid())], stdout=subprocess.PIPE).stdout.decode('utf-8'))
else:
    print('No changes detected.\nDone.')