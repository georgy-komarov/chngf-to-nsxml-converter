import sys  # sys нужен для передачи argv в QApplication

from PyQt5 import QtWidgets

import converter
import design  # Это наш конвертированный файл дизайна


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
        except BaseException as e:  # TODO: Better error message
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
                self.html_parser.parse()
                self.html_parser.get_subjects_set()
                self.fill_combobox()
                self.checkButton.setEnabled(True)
                self.statusBar.showMessage('Файлы успешно загружены!')

    def fill_combobox(self):
        self.classchoice.addItems([c.name for c in self.ns_parser.plans])
        self.classchoice.setEnabled(True)
        self.classchoice.currentTextChanged.connect(self.show_corellations)
        self.show_corellations(self.ns_parser.plans[0].name)

    def show_corellations(self, name):  # first для того, чтобы заполнить словари корелляции впервые
        self.clear_layout(self.scrollbarLayout)

        html_class = self.html_parser.get_class_by_name(name)
        ns_class = self.ns_parser.get_class_by_name(name)

        for i, ns_subject in enumerate(ns_class.plan, start=1):
            items = self.fill_subjects_combobox(ns_subject, html_class)

            horizontalLayout = QtWidgets.QHBoxLayout()
            horizontalLayout.setObjectName(f"horizontalLayout_{i}")

            subject = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            subject.setObjectName(f"subject_{i}")
            subject.setText(str(ns_subject))
            horizontalLayout.addWidget(subject)

            subject_comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
            subject_comboBox.setObjectName(f"subject_comboBox_{i}")
            subject_comboBox.addItems(items)
            subject_comboBox.currentTextChanged.connect(self.save_corellations)
            horizontalLayout.addWidget(subject_comboBox)

            self.scrollbarLayout.addLayout(horizontalLayout)

    def check(self):
        try:
            classes = self.html_parser.classes
            for c in classes:
                corellations, subjects = c.corellations, c.subjects
                if len(corellations) != len(subjects):
                    print(c.name, '!!!')  # TODO: MessageDialog

            self.convertButton.setEnabled(True)
            self.convertButton.clicked.connect(self.save_all)
        except BaseException as e:  # TODO: Better error message
            self.statusBar.showMessage('Что-то пошло не так...')

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())

    def fill_subjects_combobox(self, ns_lesson, html_class):
        html_subjects = list(html_class.subjects)
        for s in html_subjects:
            name, teacher = s.split(' — ')
            if name.lower() == ns_lesson.name.lower() and teacher == ns_lesson.teacher.name or \
                    html_class.corellations.get(s) == ns_lesson:
                valid_subject = s
                html_subjects.remove(s)
                break
        else:
            valid_subject = None

        result = [''] + sorted(list(html_subjects))  # TODO: Sort by key=x.lower()
        if valid_subject:
            result.insert(0, valid_subject)
            html_class.corellations[valid_subject] = ns_lesson
        return result

    def save_corellations(self, html_name):
        sender = self.sender()
        index = sender.objectName().split('_')[-1]

        class_name = str(self.classchoice.currentText())
        subject_label = self.findChild(QtWidgets.QLabel, f'subject_{index}')
        subject_name = str(subject_label.text())

        ns_lesson = self.ns_parser.get_lesson_by_subject_name(subject_name, class_name)
        html_class = self.html_parser.get_class_by_name(class_name)
        html_class.corellations[
            html_name] = ns_lesson  # FIXME: Fundamental bug (must swap keys and values in corellations dict)

    def save_all(self):
        timetable = []

        for day in self.ns_parser.DAYS:
            timetable.append([])
            for i in range(self.html_parser.LAST_LESSON_NUMBER):
                timetable[day.id].append([])

        for class_ in self.html_parser.classes:
            for lesson in class_.lessons:
                try:
                    timetable[lesson.day.id][lesson.number].append(class_.corellations[lesson.get_subject()].id)
                except KeyError as e:
                    pass

        for day in self.ns_parser.DAYS:  # TODO: Save to file directly
            print(f'<Day id="{day.id + 1}" name="{day.name}" wd="{day.id + 2}" >')
            for lesson_number, lessons in enumerate(timetable[day.id], start=1):
                print(f'\t<Lesson timeId="{lesson_number}">')
                for lesson_id in lessons:
                    print('\t\t' + f'<csg id="{lesson_id}"/>')
                print('\t</Lesson>')
            print('</Day>')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TimeTableApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
