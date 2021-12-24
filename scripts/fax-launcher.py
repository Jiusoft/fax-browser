"""
Original repository link: https://github.com/Jiusoft/fax-browser
Author: Jothin kumar (https://jothin-kumar.github.io)
"""
import tkinter as tk
from tkinter.messagebox import showerror
from time import sleep
from threading import Thread
from requests import get
from datetime import datetime
from os.path import exists
from os import remove, system
import platform

if exists('version'):
    with open('version', 'r') as f:
        version = f.read()
else:
    version = ''

linux = platform.system() == 'Linux'
windows = platform.system() == 'Windows'
root = tk.Tk()
root.overrideredirect(True)
root.geometry(f'400x200+{int(root.winfo_screenwidth() / 2) - 200}+{int(root.winfo_screenheight() / 2 - 100)}')
root.configure(background='green')
tk.Label(master=root, text='FAX browser', font=('Ariel', 30), bg='green').pack()
tk.Label(master=root, text='By Jiusoft', font=('Ariel', 20), bg='green').pack()
progress_label = tk.Label(master=root, text='', font=('Ariel', 15), bg='green')
progress_label.pack(side=tk.BOTTOM)


def log(message):
    now = datetime.now()
    with open('launcher-logs.txt', 'a+') as log_file:
        log_file.write(f'[{now.year}:{now.month}:{now.day}:{now.hour}:{now.minute}:{now.second}]: {message}\n')


def in_progress_msg(msg):
    def command():
        progress_label['text'] = msg
        while True:
            sleep(0.5)
            if progress_label['text'] in [msg, msg + '.', msg + '..']:
                progress_label['text'] += '.'
            elif progress_label['text'] == msg + '...':
                progress_label['text'] = msg
            else:
                break

    Thread(target=command).start()


def check_for_updates():
    in_progress_msg('Checking for updates')
    log('Checking for updates')
    latest_version = get('https://cdn.jiu-soft.com/fax-browser/latest-version.txt').text.strip('\n')
    log(f'lv - {latest_version}')
    return latest_version != version, latest_version


def fetch_launch_command():
    in_progress_msg('Fetching launch command')
    log('Fetching launch command')
    with open('launch-command', 'wb') as file:
        if linux:
            file.write(
                get('https://cdn.jiu-soft.com/fax-browser/launch-command-linux.txt', allow_redirects=True).content)
        elif windows:
            file.write(
                get('https://cdn.jiu-soft.com/fax-browser/launch-command-windows.txt', allow_redirects=True).content)
    log('Launch command fetched')


def download_update(latest_version):
    in_progress_msg('Downloading update')
    log('Downloading update')
    with open('update_temp.zip', 'wb') as file:
        file.write(get('https://cdn.jiu-soft.com/fax-browser/fax-browser-files.zip', allow_redirects=True).content)
    fetch_launch_command()
    with open('version', 'w') as file:
        file.write(latest_version)
    log('Update downloaded')


def install_update():
    in_progress_msg('Installing update')
    log('Installing update')
    import zipfile
    zip_file = zipfile.ZipFile('update_temp.zip', 'r')
    zip_file.extractall('fax-browser')
    zip_file.close()
    remove('update_temp.zip')
    log('Update installed')


def launch():
    try:
        in_progress_msg('Launching')
        log('Launching browser')
        if not exists('launch-command'):
            fetch_launch_command()
        with open('launch-command', 'r') as file:
            system(file.read())
        log('Browser launched')
    except RuntimeError:
        log('RuntimeError in function launch')
    except Exception as e:
        log(f'Error: {e}')
        showerror('Error', f'An error occurred in function launch: {e}\nPlease raise an issue on GitHub')


def main():
    try:
        updates_available, latest_version = check_for_updates()
        if updates_available:
            download_update(latest_version)
            install_update()
        Thread(target=launch).start()
        sleep(1)
        root.destroy()
    except RuntimeError:
        log('RuntimeError in function main')
    except Exception as e:
        log(f'Error: {e}')
        showerror('Error', f'An error occurred in function launch: {e}\nPlease raise an issue on GitHub')


Thread(target=main).start()
root.mainloop()
