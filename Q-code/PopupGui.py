# -*- coding: utf-8 -*-
import os
import utils

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QRect, QSize, QMetaObject
from PyQt5.QtWidgets import QWidget,\
                            QPushButton,\
                            QLineEdit,\
                            QFileDialog,\
                            QDialogButtonBox,\
                            QSizePolicy

class popupWindow(QWidget):
    """Appear when user want add new project"""
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon('images\\icon.ico'))        
        self.setObjectName("popup_window")
        self.setFixedSize(335, 85)
        self.setWindowTitle("Add project")
        self.setupUi()
        self.add_function_to_button()
        self.new_project_name = None

    def setupUi(self):
        font = QFont()
        font.setPointSize(10)
        font.setWeight(55)

        self.confirm_button = QDialogButtonBox(self)
        self.confirm_button.setGeometry(QRect(130, 40, 181, 41))
        self.confirm_button.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.confirm_button.setObjectName("confirm_button")

        self.project_name_line = QLineEdit(self)
        self.project_name_line.setGeometry(QRect(50, 10, 261, 31))
        self.project_name_line.setReadOnly(True)
        self.project_name_line.setObjectName("project_name_line")
        self.project_name_line.setPlaceholderText("Browse folder of new project.")
        self.project_name_line.setFont(font)

        self.project_browser = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, \
                                            QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.project_browser.sizePolicy().hasHeightForWidth())
        self.project_browser.setIcon(QIcon('images\\open.png'))
        self.project_browser.setIconSize(QSize(30, 30))
        self.project_browser.setGeometry(QRect(10, 10, 30, 30))
        self.project_browser.setMaximumSize(QSize(30, 30))
        self.project_browser.setSizePolicy(sizePolicy)
        self.project_browser.setFlat(True)
        self.project_browser.setObjectName("project_browser")
        
        QMetaObject.connectSlotsByName(self)

    def add_function_to_button(self):
        self.confirm_button.accepted.connect(self.on_oke)
        self.confirm_button.rejected.connect(self.on_cancel)
        self.project_browser.clicked.connect(self.browse_project)

    def get_new_project(self):
        project_name = self.project_name_line.text()
        if utils.validate_folder_name(project_name):
            self.new_project_name = project_name
        else:
            self.new_project_name = None
        
        return self.new_project_name

    def on_cancel(self):
        self.new_project_name = None
        self.close()
    
    def on_oke(self):
        self.close()

    def browse_project(self):
        link = QFileDialog.getExistingDirectory(self, "Select folder")
        self.new_project_name = os.path.basename(link)
        self.project_name_line.clear()
        self.project_name_line.setText(self.new_project_name)
