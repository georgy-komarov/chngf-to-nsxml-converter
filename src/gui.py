import sys  # sys нужен для передачи argv в QApplication

from PyQt5 import QtWidgets

import design  # Это наш конвертированный файл дизайна
import converter


class TimeTableApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.actionHTML.triggered.connect(self.set_ch_file)
        self.action_NSXML.triggered.connect(self.set_ns_file)
        self.statusBar.showMessage('Загрузите файлы расписания!')

        self.ns_parser = converter.NSParser()
        self.ch_file = None
        self.ns_file = None

    def set_ch_file(self):
        self.ch_file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл с расписанием из Хронографа",
                                                             filter="HTML файлы (*.html);;Все файлы (*)")[0]
        print(self.ch_file)

    def set_ns_file(self):
        self.ns_file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл с расписанием из Сетевого города",
                                                             filter="NSXML файлы (*.nsxml);;Все файлы (*)")[0]
        print(self.ns_file)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TimeTableApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
