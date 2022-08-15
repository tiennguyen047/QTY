# -*- coding: utf-8 -*-
import shutil, os, subprocess, time
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox

def create_tempory_folder() -> None:
    "Make temp folder if it not exist"
    if not os.path.exists("temp"):
        os.mkdir("temp")

def empty_tempory_folder():
    try:
        shutil.rmtree("temp")
        create_tempory_folder()
    except Exception as e:
        with open("log.txt", "w") as log_file:
            log_file.write(str(e) + "\n" + "def empty_tempory_folder")

def copy_branch_name_to_clipboard(text):
    subprocess.run(['clip.exe'], input = text.encode("UTF-8"), check=True)

def find_project(project_name: str, link: str) -> list():
    #Need works
    project_lib_link    = ''
    project_srcipt_link = ''

    for root, subdirs, _ in os.walk(link):
        for folder_name in subdirs:
            if folder_name == project_name:
                temp_path = os.path.join(root, folder_name)
                if "LIBRARY" in temp_path.upper() \
                    or "LIBARY" in temp_path.upper():
                    project_lib_link = temp_path
                if "PYTHONPARTSSCRIPTS" in temp_path.upper() \
                    or "PYTHONPARTSCRIPTS" in temp_path.upper() \
                    or "PYTHONPARTSSCRIPT" in temp_path.upper() \
                    or "PYTHONPARTSCRIPT" in temp_path.upper():
                    project_srcipt_link = temp_path

    return [project_lib_link, project_srcipt_link]

def get_pids(program_name : str) -> int:
    "Get process ID of VSCode to turn it off in case it is running"
    task_list = os.popen("tasklist").read().strip().split("\n")
    current_PID = []
    try:
        for task in task_list:
            if task.startswith(program_name):
                current_PID.append(int(task.split()[1]))
    except IndexError as e:
        pass

    return current_PID

def get_current_time(time_format = "Backup") -> str:
    "Return a string show the time"
    if time_format == "Backup":
        current_time = datetime.today().strftime('%m%d_%H%M')
    elif time_format == "Logging":
        current_time = datetime.today().strftime('%H:%M:%S')
    elif time_format == "database":
        current_time = time.time()
    return current_time

def get_date() -> str:
    date = datetime.today().strftime('%Y-%m-%d')
    return date

def is_exists(link_list) -> bool:
    if isinstance(link_list, list):
        for link in link_list:
            if not os.path.exists(link):
                return False
        return True
    #string
    if os.path.exists(link_list):
        return True

def show_warning_message() -> None:
    msg = QMessageBox()
    msg.setWindowTitle("Files In Use")
    msg.setText("This action can't be completed because files is opening")
    msg.setInformativeText("Close these files and try again!")
    msg.setIcon(QMessageBox.Critical)
    msg.exec_()

def show_oke_message() -> None:
    msg = QMessageBox()
    msg.setWindowTitle("Restore finish")
    msg.setText("Restore process is complete.")
    msg.setIcon(QMessageBox.Information)
    msg.exec_()
    
def validate_folder_name(name:str) -> bool:
    """Create new folder with 'name' to validate if this name is valid or not"""
    restricted_list = ["@", "$", "%", "&", "/", ":", "*", "?",
                       "\"", "\'", "<", ">", "|", "~", "`", "#", "^", 
                       "+", "=", "{", "}", "[", "]", ";", "!"]
    for char in restricted_list:
        if char in name:
            # print(char)
            return False
    try:
        temp_path = "temp\\" + name
        os.mkdir(temp_path)
    except Exception as e:
        with open("log.txt", "w") as log_file:
            log_file.write(str(e))
        return False
    #Remove created folder
    shutil.rmtree(temp_path, ignore_errors=True)
    return True
