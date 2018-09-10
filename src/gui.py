import sys  # sys нужен для передачи argv в QApplication

from PyQt5 import QtWidgets

import design  # Это наш конвертированный файл дизайна
import converter
from exceptions import *


class TimeTableApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.actionHTML.triggered.connect(self.set_ch_file)
        self.action_NSXML.triggered.connect(self.set_ns_file)
        self.checkButton.clicked.connect(self.check)
        self.load.triggered.connect(self.load_data)
        self.statusBar.showMessage('Загрузите файлы расписания!')

        self.ns_parser = converter.NSParser()
        self.html_parser = converter.HTMLParser()
        self.ch_file = None
        self.ns_file = None

    def set_ch_file(self):
        self.ch_file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл с расписанием из Хронографа",
                                                             filter="HTML файлы (*.html);;Все файлы (*)")[0]

    def set_ns_file(self):
        self.ns_file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл с расписанием из Сетевого города",
                                                             filter="NSXML файлы (*.nsxml);;Все файлы (*)")[0]

    def load_data(self):
        try:
            assert self.ch_file
            self.html_parser.load(self.ch_file)
        except:
            self.statusBar.showMessage('Ошибка загрузки HTML файла!')

        if self.html_parser.table:
            try:
                assert self.ns_file
                self.ns_parser.load(self.ns_file)
                self.ns_parser.parse_all()
            except:
                self.statusBar.showMessage('Ошибка загрузки NSXML файла!')
            else:
                self.html_parser.set_classes(self.ns_parser.plans)
                self.fill_combobox()
                self.checkButton.setEnabled(True)
                self.statusBar.showMessage('Файлы успешно загружены!')

    def fill_combobox(self):
        self.classchoice.addItems([c.name for c in self.ns_parser.plans])
        self.classchoice.setEnabled(True)
        self.classchoice.currentTextChanged.connect(self.load_corellations)
        self.load_corellations(self.ns_parser.plans[0].name)

    def load_corellations(self, name):
        self.clear_layout(self.scrollbarLayout)

        for c in self.ns_parser.plans:
            if c.name == name:
                class_ = c
                break
        else:
            raise NSLoaderException

        for i, s in enumerate(class_.plan, start=1):
            horizontalLayout = QtWidgets.QHBoxLayout()
            horizontalLayout.setObjectName(f"horizontalLayout_{i}")

            subject = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            subject.setObjectName(f"subject_{i}")
            subject.setText(str(s))
            horizontalLayout.addWidget(subject)

            subject_comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
            subject_comboBox.setObjectName(f"subject_comboBox_{i}")
            subject_comboBox.addItems(list(map(str, [i] * i)))  # TODO Change to subjects
            horizontalLayout.addWidget(subject_comboBox)

            self.scrollbarLayout.addLayout(horizontalLayout)

    def check(self):
        pass

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TimeTableApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
