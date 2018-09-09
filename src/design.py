# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(433, 532)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.classlabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.classlabel.setFont(font)
        self.classlabel.setObjectName("classlabel")
        self.horizontalLayout.addWidget(self.classlabel)
        self.classchoice = QtWidgets.QComboBox(self.centralwidget)
        self.classchoice.setEnabled(False)
        self.classchoice.setObjectName("classchoice")
        self.horizontalLayout.addWidget(self.classchoice)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 417, 379))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 433, 31))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setSizeGripEnabled(True)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionHTML = QtWidgets.QAction(MainWindow)
        self.actionHTML.setObjectName("actionHTML")
        self.action_NSXML = QtWidgets.QAction(MainWindow)
        self.action_NSXML.setObjectName("action_NSXML")
        self.load = QtWidgets.QAction(MainWindow)
        self.load.setObjectName("load")
        self.menu.addAction(self.actionHTML)
        self.menu.addAction(self.action_NSXML)
        self.menu.addSeparator()
        self.menu.addAction(self.load)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Конвертер расписания"))
        self.classlabel.setText(_translate("MainWindow", "Выберите класс:"))
        self.pushButton.setText(_translate("MainWindow", "Конвертировать"))
        self.menu.setTitle(_translate("MainWindow", "Загрузка"))
        self.actionHTML.setText(_translate("MainWindow", "HTML (Хронограф)"))
        self.action_NSXML.setText(_translate("MainWindow", "NSXML (Сетевой город)"))
        self.load.setText(_translate("MainWindow", "Загрузить"))

