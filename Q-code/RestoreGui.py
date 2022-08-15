# -*- coding: utf-8 -*-
import os, shutil
import utils

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets

class restoreWindow(QWidget):
    """Appear when user want add new project"""
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon('images\\icon.ico'))        

        self.setupUi(self)
        self.add_function_to_button()
        # self.new_project_name = None

    def backup_link(self, backup_link):
        self.backup_link = backup_link

    def local_link(self, local_link):
        self.local_link = local_link

    def project_name(self, project_name):
        self.project_name = project_name

    def on_cancel(self):
        self.close()
    
    def on_oke(self):
        try:
            if  os.path.exists(self.library_link) \
            and os.path.exists(self.scripts_link) \
            and os.path.exists(self.local_link):
                self.restore()
        except Exception as e:
            with open("log.txt", "w") as log_file:
                log_file.write(str(e) + "\n" + "def on_oke")
        self.close()

    def restore(self):
        tail_lib    = '\\Library\\PythonParts\\' + self.project_name
        tail_script = '\\PythonPartsScripts\\'   + self.project_name
        for source_link, tail in zip([self.library_link, self.scripts_link], [tail_lib, tail_script]):
            destination_link    = self.local_link + tail
            if os.path.exists(destination_link):
                try:
                    shutil.rmtree(destination_link)
                    shutil.copytree(source_link, destination_link)
                except Exception as e:
                    utils.show_warning_message()
                    with open("log.txt", "w") as log_file:
                        log_file.write(str(e) + "\n" + "def restore")
                    break
        else:
            utils.show_oke_message()

    def browse_library_folder(self):
        link = QFileDialog.getExistingDirectory(self, 
                                                "Select backup version in library folder",  
                                                self.backup_link)

        if len(link) != 0:
            self.lineEdit.clear()
            self.lineEdit.setText(link)
            self.lineEdit.setCursorPosition(len(link)-1)
            self.library_link = link

    def browse_scripts_folder(self):
        link = QFileDialog.getExistingDirectory(self, 
                                                "Select backup version in scripts folder",  
                                                self.backup_link)
        if len(link) != 0:
            self.lineEdit_2.clear()
            self.lineEdit_2.setText(link)
            self.lineEdit_2.setCursorPosition(len(link)-1)
            self.scripts_link = link

    def add_function_to_button(self):
        self.confirm_button.accepted.connect(self.on_oke)
        self.confirm_button.rejected.connect(self.on_cancel)
        self.browse_library_button.clicked.connect(self.browse_library_folder)
        self.browse_scripts_button.clicked.connect(self.browse_scripts_folder)

    def setupUi(self, restoreWindow):
        restoreWindow.setObjectName("restoreWindow")
        restoreWindow.resize(535, 120)
        self.verticalLayout = QtWidgets.QVBoxLayout(restoreWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(restoreWindow)
        self.frame_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_lib_link = QtWidgets.QLabel(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_lib_link.sizePolicy().hasHeightForWidth())
        self.label_lib_link.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_lib_link.setFont(font)
        self.label_lib_link.setObjectName("label_lib_link")
        self.horizontalLayout_3.addWidget(self.label_lib_link)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.browse_library_button = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browse_library_button.sizePolicy().hasHeightForWidth())
        self.browse_library_button.setSizePolicy(sizePolicy)
        self.browse_library_button.setToolTipDuration(-1)
        self.browse_library_button.setText("")
        self.browse_library_button.setIcon(QIcon('images\\open.png'))
        self.browse_library_button.setIconSize(QtCore.QSize(30, 30))
        self.browse_library_button.setAutoDefault(False)
        self.browse_library_button.setDefault(False)
        self.browse_library_button.setFlat(True)
        self.browse_library_button.setObjectName("browse_library_button")
        self.horizontalLayout_3.addWidget(self.browse_library_button)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame = QtWidgets.QFrame(restoreWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_script_link = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_script_link.sizePolicy().hasHeightForWidth())
        self.label_script_link.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_script_link.setFont(font)
        self.label_script_link.setObjectName("label_script_link")
        self.horizontalLayout_4.addWidget(self.label_script_link)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setClearButtonEnabled(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_4.addWidget(self.lineEdit_2)
        self.browse_scripts_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browse_scripts_button.sizePolicy().hasHeightForWidth())
        self.browse_scripts_button.setSizePolicy(sizePolicy)
        self.browse_scripts_button.setToolTipDuration(-1)
        self.browse_scripts_button.setText("")
        self.browse_scripts_button.setIcon(QIcon('images\\open.png'))
        self.browse_scripts_button.setIconSize(QtCore.QSize(30, 30))
        self.browse_scripts_button.setFlat(True)
        self.browse_scripts_button.setObjectName("browse_scripts_button")
        self.horizontalLayout_4.addWidget(self.browse_scripts_button)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(restoreWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setContentsMargins(5, 0, -1, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.confirm_button = QtWidgets.QDialogButtonBox(self.frame_2)
        self.confirm_button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirm_button.setObjectName("confirm_button")
        self.horizontalLayout_5.addWidget(self.confirm_button, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignRight)

        self.retranslateUi(restoreWindow)
        QtCore.QMetaObject.connectSlotsByName(restoreWindow)

    def retranslateUi(self, restoreWindow):
        restoreWindow.setWindowTitle("Restore from backup")
        self.label_lib_link.setText("Library folder")
        self.browse_library_button.setToolTip("Click to browse library folder")
        self.label_script_link.setText("Scripts folder")
        self.browse_scripts_button.setToolTip("Click to browse scripts folder")

    # def get_new_project(self):
    #     project_name = self.project_name_line.text()
    #     if utils.validate_folder_name(project_name):
    #         self.new_project_name = project_name
    #     else:
    #         self.new_project_name = None
        
    #     return self.new_project_name

    # def browse_project(self):
    #     link = QFileDialog.getExistingDirectory(self, "Select folder")
    #     self.new_project_name = os.path.basename(link)
    #     self.project_name_line.clear()
    #     self.project_name_line.setText(self.new_project_name)
