
# -*- coding: utf-8 -*-
#import python library
import shutil, os, json, time
#import from PyQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QEventLoop, QThread
from PyQt5.QtWidgets import QApplication, QFileDialog
#Local import
import utils
from NewGUI import NewGUI
from record import Record
from working_data import Data
from PopupGui import popupWindow
from addTaskGui import addTaskGui
from RestoreGui import restoreWindow
from thread import ThreadClass, HardWorker
#code render
#pyinstaller --onefile --windowed --icon=icon.ico main.py
CURRENT_BRANCHE_INFO = '\\.git\\HEAD'
#Folder to get branche info

from PyQt5 import QtCore, QtGui

class MainWindow(NewGUI):
    EXIT_CODE_REBOOT = -123
    def __init__(self):
        super().__init__()
        self.add_function_to_button()
        
        self.time_start               = time.time()
        self.working_branche_duration = {}
        self.branche_start_time       = {}
        self.pids                     = utils.get_pids("Code.exe")
        self.on_workspace             = False
        self.last_mtime               = 0.0 #Modify time of file git info
        self.current_branche          = None
        utils.create_tempory_folder()

        self.connect_database()
        self.thread = ThreadClass(parent=None,index=1)
        self.thread.any_signal.connect(self.get_current_branch)
        # self.thread_2 = ThreadSecond(parent=None,index=1)
        # self.thread_2.any_signal.connect(self.aut)
        self.load_last_setting()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
           self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
           event.accept()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.button() == 0:#QtCore.Qt.LeftButton:
           self.move(event.globalPos() - self.dragPosition)
           event.accept()

    def on_close(self):
        duration    = self.data.get_record_property(self.current_branche, "duration")
        start_time  = self.data.get_record_property(self.current_branche, "start_time")
        duration   += int(utils.get_current_time("database") - start_time)
        self.data.update_record(self.current_branche, "duration", duration)

        self.data.print_table()
        self.data.close_connect()
        self.close()
    
    def on_minimize(self):
        self.showMinimized()

    def keyPressEvent(self,e):
        if (e.key() == Qt.Key_R):
            QApplication.exit( MainWindow.EXIT_CODE_REBOOT )
    
    def wheelEvent(self, e: QtGui.QWheelEvent):
        self.logging_window.wheelEvent(e)
        
    def moveEvent(self, event):
        self.stop_worker()

    def hideEvent(self, event):
        self.stop_worker()

    def showEvent(self, event):
        self.start_worker()

    def add_task(self, event):
        self.stop_worker()
        self.popup_3 = addTaskGui()
        self.popup_3.show()
        
        loop = QEventLoop()
        self.popup_3.destroyed.connect(loop.quit)
        loop.exec()  # wait until popup closed

    def work_space(self):
        if self.on_workspace:
            #Click to close workspace
            try:
                for i in self.pids:
                    os.kill(i, 21)
            except Exception as e:
                with open("log.txt", "w") as log_file:
                    log_file.write(str(e) + "\n" + "def work_space close workspace")
            self.on_workspace = False
            self.WorkSpace.setToolTip("Click to open workspace.")
            self.WorkSpace.setIcon(QIcon("images\\off_workspace.png"))
            self.WorkSpace.setIconSize(QSize(30, 30))
        else:
            #Click to open workspace
            self.on_workspace = True
            self.WorkSpace.setToolTip("Workspace is opening.\nClick to close workspace.")
            self.WorkSpace.setIcon(QIcon("images\\on_workspace.png"))
            self.WorkSpace.setIconSize(QSize(30, 30))
            try:
                os.startfile('local.code-workspace')
                self.pids = utils.get_pids("Code.exe")
            except Exception as e:
                with open("log.txt", "w") as log_file:
                    log_file.write(str(e) + "\n" + "def work_space open workspace")

    def restore_from_backup(self):
        self.popup_2 = restoreWindow()
        self.popup_2.backup_link(self.link_backup)
        self.popup_2.local_link(self.link_local)
        self.popup_2.project_name(self.project_list.currentText())
        self.popup_2.show()
        
        loop = QEventLoop()
        self.popup_2.destroyed.connect(loop.quit)
        loop.exec() # wait until popup closed

    def project_adding_popup_window(self):
        self.popup_1 = popupWindow()
        self.popup_1.show()
        
        loop = QEventLoop()
        self.popup_1.destroyed.connect(loop.quit)
        loop.exec() # wait until popup closed

        new_project = self.popup_1.get_new_project()
        if new_project is not None and new_project not in self.proj_list:
            self.proj_list.append(new_project)
            self.save_user_setting()

    def git_browser(self):
        self.stop_worker()
        link = QFileDialog.getExistingDirectory(self,
                                                "Select git folder", 
                                                os.path.dirname(self.link_git))
        if len(link) != 0:
            self.link_git = link
            self.GitLink.clear()
            self.GitLink.setText(self.link_git)
            self.GitLink.setCursorPosition(0)
            self.save_user_setting()
            self.get_current_branch()
            self.update_workspace_state()
        self.start_worker()
        self.button_control()

    def local_browser(self):
        link = QFileDialog.getExistingDirectory(self, 
                                                "Select local(etc) folder", 
                                                os.path.dirname(self.link_local))
        if len(link) != 0:
            self.link_local = link
            self.LocalLink.clear()
            self.LocalLink.setText(self.link_local)
            self.LocalLink.setCursorPosition(0)
            self.button_control()
            self.save_user_setting()
        else:
            self.button_control()

    def backup_browser(self):
        link = QFileDialog.getExistingDirectory(self, 
                                                "Select backup folder", 
                                                os.path.dirname(self.link_backup))
        if len(link) != 0:
            self.link_backup = link
            self.BackupLink.clear()
            self.BackupLink.setText(self.link_backup)
            self.BackupLink.setCursorPosition(0)
            self.save_user_setting()
        self.button_control()

    def auto_backup(self):
        self.stop_worker()
        project_name = self.project_list.currentText()
        tail_lib    = '\\Library\\PythonParts\\' + project_name
        tail_script = '\\PythonPartsScripts\\'   + project_name
        for tail in [tail_lib, tail_script]:
            source_link      = self.link_local + tail
            destination_link = "temp" + tail + '_' + utils.get_current_time()
            if os.path.exists(source_link):
                shutil.copytree(source_link, destination_link, ignore=shutil.ignore_patterns(str(self.ignore_patterns)[1:-1]), dirs_exist_ok=True)

        self.start_worker()
    
    #Long-running task
    def backup(self):
        self.stop_worker()
        project_name = self.project_list.currentText()
        tail_lib    = '\\Library\\PythonParts\\' + project_name
        tail_script = '\\PythonPartsScripts\\'   + project_name
        for tail in [tail_lib, tail_script]:
            source_link      = self.link_local + tail
            destination_link = self.link_backup + tail + '_' + utils.get_current_time()
            if os.path.exists(source_link):
                try:
                    if os.path.exists(destination_link):
                        shutil.rmtree(destination_link)
                    shutil.copytree(source_link, destination_link, ignore=shutil.ignore_patterns(str(self.ignore_patterns)[1:-1]), dirs_exist_ok=True)
                except Exception as e:
                    self.logging_window.appendPlainText("x"*20 +" Backup Unsuccessful " + "x"*20)
                    with open("log.txt", "w") as log_file:
                        log_file.write(str(e) + "\n" + "def backup")
                    utils.show_warning_message()
            else:
                break 
        else:     
            dash_number = 31
            self.logging_window.appendPlainText("Backup successfully " +\
                                                "<-" + "-"*dash_number +\
                                                utils.get_current_time("Logging") +\
                                                "-"*dash_number + ">")
        self.start_worker()
    
    #Long-running task
    def check_in(self):
        self.stop_worker()
        for source_link, destination_link in zip(self.local_result, self.git_result):
            try:
                # shutil.rmtree(destination_link)
                shutil.copytree(source_link, destination_link, ignore=shutil.ignore_patterns(str(self.ignore_patterns)[1:-1]), dirs_exist_ok=True)
            except Exception as e:
                self.logging_window.appendPlainText("x"*20 +" Commit Unsuccessful " + "x"*20)
                with open("log.txt", "w") as log_file:
                    log_file.write(str(e) + "\n" + "def check_in")
                utils.show_warning_message()
        else:
            dash_number = 31
            self.logging_window.appendPlainText("Check-in successfully " +\
                                                "<-" + "-"*dash_number +\
                                                utils.get_current_time("Logging") +\
                                                "-"*dash_number + ">")
            utils.copy_branch_name_to_clipboard(self.current_branche)
        self.start_worker()
    
    #Long-running task    
    def checkout(self):
        #Backup to tempory folder temp
        self.stop_worker()
        self.auto_backup()
        for source_link, destination_link in zip(self.git_result, self.local_result):
            try:
                shutil.rmtree(destination_link)
                shutil.copytree(source_link, destination_link, ignore=shutil.ignore_patterns(str(self.ignore_patterns)[1:-1]))
            except Exception as e:
                self.logging_window.appendPlainText("x"*20 +" Checkout Unsuccessful " + "x"*20)
                with open("log.txt", "w") as log_file:
                    log_file.write(str(e) + "\n" + "def check_out")
                utils.show_warning_message()
        else:
            dash_number = 31
            self.logging_window.appendPlainText("Checkout successfully " +\
                                                "<-" + "-"*dash_number +\
                                                utils.get_current_time("Logging") +\
                                                "-"*dash_number + ">")

        self.start_worker()

    def save_user_setting(self):
        data = {"link_git": self.link_git,
                "link_local": self.link_local,
                "link_backup": self.link_backup,
                "proj_list": self.proj_list,
                "ignore_patterns": self.ignore_patterns
                }
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=False)
        try:
            workspace_data = {
                "folders": [{
                    "path": self.local_result[0]
                },
                {
                    "path": self.local_result[1]
                }],
                "settings": {}
            }
            with open('local.code-workspace', 'w') as f:
                json.dump(workspace_data, f, indent=4, sort_keys=False)
        except Exception as e:
            with open("log.txt", "w") as log_file:
                log_file.write(str(e) + "\n" + "def save_user_setting")

    def load_last_setting(self):
        if os.path.exists('working_time.json'):
            with open('working_time.json') as data_file:
                data_loaded = json.load(data_file)
        if os.path.exists('data.json'):
            with open('data.json') as data_file:
                data_loaded = json.load(data_file)
                #Load last links
                for i in ["link_git", "link_backup", "link_local"]:
                    if i in data_loaded.keys() and os.path.exists(data_loaded[i]):
                        exec("self."+ i +" = data_loaded[i]")
                    else:
                        exec("self."+ i +" = ''")
                #Load ignore patterns
                if "ignore_patterns" in data_loaded.keys():
                    self.ignore_patterns = data_loaded["ignore_patterns"]
                else:
                    self.ignore_patterns = ['*.pyc', '*.txt', '___pyp__', '*.db']
                self.BackupLink.setText(self.link_backup)
                self.LocalLink.setText(self.link_local)
                self.GitLink.setText(self.link_git)
                #To focus on the left
                self.BackupLink.setCursorPosition(0)
                self.LocalLink.setCursorPosition(0)
                self.GitLink.setCursorPosition(0)
                #Get branch info
                self.get_current_branch()
                self.update_workspace_state()
                #Load list of projects
                self.proj_list = data_loaded["proj_list"]
        else:
            self.link_git    = ''
            self.link_backup = ''
            self.link_local  = ''
            self.proj_list = ["Automated Reinforcement", "Prefabrication", "StructuralFraming"]
            self.ignore_patterns = ['*.pyc', '*.txt', '___pyp__', '*.db']
        
        self.project_list.addItems(self.proj_list)
        self.button_control()
        self.start_worker()

    def update_workspace_state(self) -> None:
        "Check if VSCode is opening or not"
        if not utils.get_pids("Code.exe"):
            self.on_workspace = False
            self.WorkSpace.setToolTip("Click to open workspace.")
            self.WorkSpace.setIcon(QIcon("images\\off_workspace.png"))
            self.WorkSpace.setIconSize(QSize(30, 30))
        else:
            self.on_workspace = True
            self.WorkSpace.setToolTip("Workspace is opening.\nClick to close workspace.")
            self.WorkSpace.setIcon(QIcon("images\\on_workspace.png"))
            self.WorkSpace.setIconSize(QSize(30, 30))

    def get_current_branch(self) -> None:
        link = self.link_git + CURRENT_BRANCHE_INFO
        dash_number = 71 #This magic number of dash will fill up 1 line in console.
        if os.path.exists(link):
            last_mtime = os.path.getmtime(link)
            if last_mtime != self.last_mtime:
                #Remove all auto backup file whenever user change to another branch
                utils.empty_tempory_folder()
                self.last_mtime = last_mtime
                file = open(link, "r")
                #Save last working branche
                self.last_working_branche = self.current_branche
                self.current_branche = file.readline().split('/')[-1].strip()
                #Consider to place connect_function to GUI __init__, place update database function here
                try:
                    self.update_database()
                except Exception as e:
                    print(e)
                    with open("log.txt", "w") as log_file:
                        log_file.write(str(e) + "\n" + "def update_database")

                self.logging_window.appendPlainText("Current branche:\n" + \
                                                self.current_branche + \
                                                " <" + "-"*dash_number + ">")
                file.close()
        else:
            self.logging_window.setPlainText("Current branche:\n" + \
                                            "Local directory (not git's directory) " + \
                                            "<" + "-"*dash_number + ">")
        self.update_workspace_state()

    def connect_database(self):
        #  Make connection
        self.data = Data()
        if utils.is_exists("working_time.db"):
            self.data.connect_sql()
        else:
            self.data.connect_sql()
            #Create new database
            self.data.create_table()
        
    def update_database(self):
        #  Update database
        branch_name = self.current_branche
        last_working_branch = self.last_working_branche

        #Just open app so last_working_branch = None, New working branch -> add to database
        if not self.data.is_exist_record(branch_name) and last_working_branch == None:
            new_record = Record(branch_name, utils.get_current_time("database"), utils.get_date())
            self.data.insert_record(new_record)
            return

        #Just open app so last_working_branch = None, Still open last branch -> update start_time
        if self.data.is_exist_record(branch_name) and last_working_branch == None:
            self.data.update_record(branch_name, "start_time", utils.get_current_time("database"))
            return

        #App is running, New working branch -> add to database, update duration for last_working_branch
        if not self.data.is_exist_record(branch_name):
            new_record = Record(branch_name, utils.get_current_time("database"), utils.get_date())
            self.data.insert_record(new_record)
            #Update duration for last_working_branch
            duration        = self.data.get_record_property(last_working_branch, "duration")
            last_start_time = self.data.get_record_property(last_working_branch, "start_time")
            duration       += int(self.last_mtime - last_start_time)
            self.data.update_record(last_working_branch, "duration", duration)
            return

        #Exist branch but "branch_name" = last_working_branch, it mean keep working with current branch
        if last_working_branch == branch_name:
            #Same branch was checkout -> Update duration
            duration    = self.data.get_record_property(branch_name, "duration")
            start_time  = self.data.get_record_property(branch_name, "start_time")
            duration   += int(self.last_mtime - start_time)
            self.data.update_record(branch_name, "duration", duration)
            return

        #Exist branch but "branch_name" != last_working_branch, it mean work with new_branch
        if last_working_branch != branch_name:
            #Update duration for last_working_branch
            duration        = self.data.get_record_property(last_working_branch, "duration")
            last_start_time = self.data.get_record_property(last_working_branch, "start_time")
            duration       += int(self.last_mtime - last_start_time)
            self.data.update_record(last_working_branch, "duration", duration)
            #Update start_time for new branch
            self.data.update_record(branch_name, "start_time", self.last_mtime)
        
    def start_worker(self):
        self.thread.start()

    def stop_worker(self):
        self.thread.stop()

    def turn_off_main_buttons(self):
        self.Checkout.setEnabled(False)
        self.Checkin.setEnabled(False)
        self.Backup.setEnabled(False)

    def turn_on_main_buttons(self):
        self.Checkout.setEnabled(True)
        self.Checkin.setEnabled(True)
        self.Backup.setEnabled(True)
        
    def button_control(self):
        "Control the enable state of button in main window"
        project_name = self.project_list.currentText()
        if utils.is_exists([self.link_git, self.link_local]):
            if self.link_git != self.link_local:
                git_result = utils.find_project(project_name, self.link_git)
                local_result = utils.find_project(project_name, self.link_local)
                if utils.is_exists(git_result + local_result):
                    self.Checkout.setEnabled(True)
                    self.Checkin.setEnabled(True)
                    self.WorkSpace.setEnabled(True)
                    self.git_result = git_result
                    self.local_result = local_result
                else:
                    self.Checkout.setEnabled(False)
                    self.Checkin.setEnabled(False)
                    self.WorkSpace.setEnabled(False)
            else:
                self.Checkout.setEnabled(False)
                self.Checkin.setEnabled(False)
                self.WorkSpace.setEnabled(False)
        
        if utils.is_exists([self.link_backup, self.link_local]):
            if self.link_backup != self.link_local and \
                utils.is_exists(utils.find_project(project_name, self.link_local)):
                self.Backup.setEnabled(True)
                self.Restore_button.setEnabled(True)
                self.WorkSpace.setEnabled(True)
            else:
                self.Backup.setEnabled(False)
                self.Restore_button.setEnabled(False)
                self.WorkSpace.setEnabled(False)

    def add_function_to_button(self):

        """Binding function to buttons and load last setting"""
        self.Backup.clicked.connect(self.runLongTask)
        self.Close.clicked.connect(self.on_close)
        self.Checkin.clicked.connect(self.runLongTask)
        self.AddTask.clicked.connect(self.add_task)
        self.Checkout.clicked.connect(self.runLongTask)
        self.Minimize.clicked.connect(self.on_minimize)
        self.WorkSpace.clicked.connect(self.work_space)
        self.GitBrowser.clicked.connect(self.git_browser)
        self.LocalBrowser.clicked.connect(self.local_browser)
        self.BackupBrowser.clicked.connect(self.backup_browser)
        self.Restore_button.clicked.connect(self.restore_from_backup)
        self.AddProject.clicked.connect(self.project_adding_popup_window)
        self.project_list.currentTextChanged.connect(self.button_control)

    def runLongTask(self):
        sender = self.sender()
        
        # Step 2: Create a QThread object
        self.long_task_thread = QThread()
        # Step 3: Create a worker object
        self.long_task_worker = HardWorker()
        self.long_task_worker.get_task(self, def_dict[sender.objectName()])
        
        # Step 4: Move worker to the thread
        self.long_task_worker.moveToThread(self.long_task_thread)
        # Step 5: Connect signals and slots
        self.long_task_thread.started.connect(self.long_task_worker.run)
        self.long_task_worker.finished.connect(self.long_task_thread.quit)
        
        self.long_task_worker.finished.connect(self.long_task_worker.deleteLater)
        self.long_task_thread.finished.connect(self.long_task_thread.deleteLater)
        self.long_task_thread.finished.connect(self.turn_on_main_buttons)
        # self.long_task_worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.long_task_thread.start()
        # Final resets
        self.turn_off_main_buttons()

def_dict = {
    "Backup": "backup()",
    "Checkin": "check_in()",
    "Checkout": "checkout()",
}