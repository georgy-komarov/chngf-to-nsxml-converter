import sys  # sys нужен для передачи argv в QApplication
import traceback

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

    def save_ns_file(self):
        try:
            name = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить файл',
                                                         filter="NSXML файл (*.nsxml);;Все файлы (*)")[0]
            result = self.save_all()

            with open(name, 'w', encoding='windows-1251') as f:
                f.write(result)

            self.statusBar.showMessage('Файл сохранён!')
        except BaseException as e:
            msg = 'Ошибка сохранения файла! Отправьте лог на georgy.komarov@mail.ru'
            error = traceback.format_exc()

            with open('error.log', 'a') as log:
                log.write(msg + '\n\n' + error)
            self.statusBar.showMessage(msg)

    def load_data(self):
        try:
            assert self.ch_file
            self.html_parser.load(self.ch_file)
        except BaseException as e:
            msg = 'Ошибка загрузки HTML файла! Отправьте лог на georgy.komarov@mail.ru'
            error = traceback.format_exc()

            with open('error.log', 'a') as log:
                log.write(msg + '\n\n' + error)
            self.statusBar.showMessage(msg)

        if self.html_parser.table:
            try:
                assert self.ns_file
                self.ns_parser.load(self.ns_file)
                self.ns_parser.parse_all()
            except:
                msg = 'Ошибка загрузки NSXML файла!'
                error = traceback.format_exc()

                with open('error.log', 'a') as log:
                    log.write(msg + '\n\n' + error)
                self.statusBar.showMessage(msg)
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

    def show_corellations(self, name):  # name - номер+буква класса
        self.clear_layout(self.scrollbarLayout)

        html_class = self.html_parser.get_class_by_name(name)
        ns_class = self.ns_parser.get_class_by_name(name)

        for i, ns_lesson in enumerate(ns_class.plan, start=1):
            items = self.fill_subjects_combobox(ns_lesson, html_class)

            horizontalLayout = QtWidgets.QHBoxLayout()
            horizontalLayout.setObjectName(f"horizontalLayout_{i}")

            subject = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            subject.setObjectName(f"subject_{i}")
            subject.setText(f'{ns_lesson} [{ns_lesson.teacher.name}]')
            horizontalLayout.addWidget(subject)

            subject_comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
            subject_comboBox.setObjectName(f"subject_comboBox_{i}")
            subject_comboBox.addItems(items)
            subject_comboBox.currentTextChanged.connect(self.save_corellations)
            horizontalLayout.addWidget(subject_comboBox)

            self.scrollbarLayout.addLayout(horizontalLayout)

    def check(self):
        try:
            not_completed = []
            classes = self.html_parser.classes
            for c in classes:
                corellations, subjects = c.corellations, c.subjects
                if len(corellations) != len(subjects):
                    not_completed.append(c.name)
            if not_completed:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Внимание!")
                msg.setInformativeText(f'В классах {", ".join(not_completed)} заполнены не все предметы!')
                msg.exec_()

            self.convertButton.setEnabled(True)
            self.convertButton.clicked.connect(self.save_ns_file)
        except BaseException as e:
            msg = 'Что-то пошло не так...'
            error = traceback.format_exc()

            with open('error.log', 'a') as log:
                log.write(msg + '\n\n' + error)
            self.statusBar.showMessage(msg)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())

    def fill_subjects_combobox(self, ns_lesson, html_class):
        def smart_sort(subject):
            subject, teacher = subject.split(' — ')
            subject = subject.lower()
            if teacher[-1].isdigit():
                digit = int(teacher[-1])
            else:
                digit = 0
            return tuple([subject, digit])

        html_subjects = list(html_class.subjects)
        for subject in html_subjects:
            name, teacher = subject.split(' — ')
            if name.lower() == ns_lesson.name.lower() and teacher == ns_lesson.teacher.name or \
                    html_class.corellations.get(ns_lesson) == subject:  # учитываем сохраненное значение
                valid_subject = subject
                html_subjects.remove(subject)
                break
        else:
            valid_subject = None

        result = [''] + sorted(list(html_subjects), key=smart_sort)
        if valid_subject:
            result.insert(0, valid_subject)
            html_class.corellations[ns_lesson] = valid_subject
        return result

    def save_corellations(self, html_name):
        sender = self.sender()
        index = sender.objectName().split('_')[-1]

        class_name = str(self.classchoice.currentText())
        subject_label = self.findChild(QtWidgets.QLabel, f'subject_{index}').text()
        subject_name, teacher_name = subject_label.split(' [')

        ns_lesson = self.ns_parser.get_lesson_by_subject_name(subject_name, class_name)
        html_class = self.html_parser.get_class_by_name(class_name)
        html_class.corellations[
            ns_lesson] = html_name

    def save_all(self):
        timetable = []

        for day in self.ns_parser.DAYS:
            timetable.append([])
            for i in range(self.html_parser.LAST_LESSON_NUMBER):
                timetable[day.id].append([])

        for class_ in self.html_parser.classes:
            reversed_corellations = {v: k for k, v in
                                     class_.corellations.items()}  # Переворачиваем словарь для текущего класса
            for lesson in class_.lessons:  # HTMLLesson День[№ урока] - Предмет (учитель)
                try:
                    day_num_lessons = timetable[lesson.day.id][lesson.number]  # Список уроков (день, номер)
                    day_num_lessons.append(reversed_corellations[lesson.get_subject()].id)
                except KeyError as e:
                    pass

        timetable_result = ''
        for day in self.ns_parser.DAYS:  # TODO: Save to file directly
            timetable_result += f'<Day id="{day.id + 1}" name="{day.name}" wd="{day.id + 2}" >\n'
            for lesson_number, lessons in enumerate(timetable[day.id], start=1):
                timetable_result += f'\t<Lesson timeId="{lesson_number}">\n'
                for lesson_id in lessons:
                    timetable_result += '\t\t' + f'<csg id="{lesson_id}"/>\n'
                timetable_result += '\t</Lesson>\n'
            timetable_result += '</Day>\n'

        with open(self.ns_file, encoding='windows-1251') as f:
            ns_file = f.readlines()

        week_block_start = None
        week_block_end = None

        for i, j in enumerate(ns_file):
            if week_block_start is None and j.strip().lower().startswith('<week'):
                week_block_start = i
            elif week_block_end is None and j.strip().lower().startswith('</week>'):
                week_block_end = i

        result = ''.join(ns_file[:week_block_start + 1]) + timetable_result + ''.join(ns_file[week_block_end:])
        return result


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TimeTableApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
