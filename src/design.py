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
        MainWindow.resize(720, 565)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_top = QtWidgets.QHBoxLayout()
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")
        self.classlabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.classlabel.setFont(font)
        self.classlabel.setObjectName("classlabel")
        self.horizontalLayout_top.addWidget(self.classlabel)
        self.classchoice = QtWidgets.QComboBox(self.centralwidget)
        self.classchoice.setEnabled(False)
        self.classchoice.setObjectName("classchoice")
        self.horizontalLayout_top.addWidget(self.classchoice)
        self.verticalLayout.addLayout(self.horizontalLayout_top)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 704, 410))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollbarLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollbarLayout.setObjectName("scrollbarLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_bottom = QtWidgets.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setEnabled(False)
        self.checkButton.setObjectName("checkButton")
        self.horizontalLayout_bottom.addWidget(self.checkButton)
        self.convertButton = QtWidgets.QPushButton(self.centralwidget)
        self.convertButton.setEnabled(False)
        self.convertButton.setObjectName("convertButton")
        self.horizontalLayout_bottom.addWidget(self.convertButton)
        self.verticalLayout.addLayout(self.horizontalLayout_bottom)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 720, 31))
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
        self.checkButton.setText(_translate("MainWindow", "Проверить"))
        self.convertButton.setText(_translate("MainWindow", "Конвертировать"))
        self.menu.setTitle(_translate("MainWindow", "Загрузка"))
        self.actionHTML.setText(_translate("MainWindow", "HTML (Хронограф)"))
        self.action_NSXML.setText(_translate("MainWindow", "NSXML (Сетевой город)"))
        self.load.setText(_translate("MainWindow", "Загрузить"))

