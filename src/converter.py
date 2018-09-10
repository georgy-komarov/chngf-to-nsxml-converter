from bs4 import BeautifulSoup
from bs4 import NavigableString

from exceptions import *


# NSParser classes
class Day:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class NSRoom:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class NSSubject:
    def __init__(self, id, name, abbr):
        self.id = id
        self.name = name
        self.abbr = abbr
        self.teachers = []

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def __str__(self):
        return self.name


class NSTeacher:
    def __init__(self, id, firstname, lastname, midname):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.midname = midname
        self.name = f'{lastname} {firstname[0]}.{midname[0]}.'

    def __str__(self):
        return self.name


class NSLesson:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.teacher = None
        self.subject = None

    def set_teacher(self, teachers, id):
        for teacher in teachers:
            if teacher.id == id:
                self.teacher = teacher

    def set_subject(self, subjects, id):
        for subject in subjects:
            if subject.id == id:
                self.subject = subject

    def __str__(self):
        return self.name


class NSClass:
    def __init__(self, id, name, boys, girls):
        self.id = id
        self.name = name.upper()
        self.grade, self.letter = int(self.name[:-1]), self.name[-1]
        self.boys = int(boys)
        self.girls = int(girls)
        self.students = self.boys + self.girls

        self.plan = []
        self.timetable_subjects = set()

    def add_lesson(self, lesson):
        self.plan.append(lesson)

    def __str__(self):
        return self.name


# HTML class
class HTMLLesson:
    def __init__(self, name, teacher, room, day, number):
        self.name = name

        self.teacher_with_group = teacher
        try:
            self.group_number, self.teacher = teacher.split(':')
        except ValueError:
            self.group_number, self.teacher = None, teacher

        self.room = room.lower()

        self.day = day
        self.number = number

    def get_subject(self):
        return f'{self.name} — {self.teacher_with_group}'

    def __str__(self):
        return f'[{self.day.name.title()}][{self.number}] - {self.name} ({self.teacher_with_group})'

    def __repr__(self):
        return str(self)


class HTMLClass:
    def __init__(self, name):
        self.name = name
        self.lessons = []
        self.subjects = set()

        self.corellations = {}

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def add_subject(self, subject):
        self.subjects.add(subject)

    def __str__(self):
        return self.name


class TimetableConverter:
    DAYS = [Day(i, d) for i, d in enumerate(['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'])]
    LAST_LESSON_NUMBER = None
    WORKING_DAYS_NUMBER = None


class NSParser(TimetableConverter):
    def __init__(self):
        self.ns = None

        self.rooms = None
        self.teachers = None
        self.subjects = None
        self.plans = None

    def load(self, filename):
        with open(filename, encoding='windows-1251') as f:
            ns = BeautifulSoup(f, 'lxml').find('timetableexchange').contents[1::2]
        self.ns = ns

    def get_teachers(self):
        teachers = []
        for tag in self.ns:
            if tag.name == 'teachers':
                teachers_tag = tag
                break
        else:
            raise NSParserException

        teachers_tags = teachers_tag.contents[1::2]
        for teacher in teachers_tags:
            teachers.append(NSTeacher(teacher.attrs['tid'], teacher.attrs['firstname'], teacher.attrs['lastname'],
                                      teacher.attrs['middlename']))

        return teachers

    def get_rooms(self):
        rooms = []
        for tag in self.ns:
            if tag.name == 'rooms':
                rooms_tag = tag
                break
        else:
            raise NSParserException

        rooms_tags = rooms_tag.contents[1::2]
        for room in rooms_tags:
            rooms.append(NSRoom(room.attrs['id'], room.attrs['name']))

        return rooms

    def get_subjects(self):
        subjects = []
        for tag in self.ns:
            if tag.name == 'subjects':
                subjects_tag = tag
                break
        else:
            raise NSParserException

        subjects_tags = subjects_tag.contents[1::2]
        for subject in subjects_tags:
            subjects.append(NSSubject(subject.attrs['sid'], subject.attrs['name'], subject.attrs['abbr']))

        return subjects

    def get_plan(self):
        plans = []
        for tag in self.ns:
            if tag.name.lower() == 'plan':
                plan_tag = tag
                break
        else:
            raise NSParserException

        plan_tags = plan_tag.contents[1::2]

        for class_tag in plan_tags:
            class_ = NSClass(class_tag.attrs['id'], class_tag.attrs['name'], class_tag.attrs['boys'],
                             class_tag.attrs['girls'])

            lessons_tags = class_tag.contents[1::2]
            for lesson_tag in lessons_tags:
                lesson = NSLesson(lesson_tag.attrs['id'], lesson_tag.attrs['name'])
                lesson.set_teacher(self.teachers, lesson_tag.attrs['tid'])
                lesson.set_subject(self.subjects, lesson_tag.attrs['sid'])
                class_.add_lesson(lesson)

            plans.append(class_)

        return plans

    def get_class_by_name(self, name):
        for c in self.plans:
            if c.name == name:
                return c
        else:
            raise NSLoaderException

    def get_lesson_by_subject_name(self, subject_name, class_name):
        class_ = self.get_class_by_name(class_name)
        subjects = class_.plan

        for s in subjects:
            if subject_name == s.name:
                return s
        else:
            raise NSLoaderException

    def parse_all(self):
        self.rooms = self.get_rooms()
        self.teachers = self.get_teachers()
        self.subjects = self.get_subjects()
        self.plans = self.get_plan()


class HTMLParser(TimetableConverter):
    def __init__(self):
        self.table = None
        self.classes = []

    def load(self, filename):
        with open(filename, encoding='windows-1251') as f:
            rasp = BeautifulSoup(f, 'lxml')

        full_table = list(rasp.find('table'))[::2]
        class_names, lessons = full_table[2], full_table[3:]

        week_column_1 = rasp.find('td', {'style': ';text-align:left'})  # Блок с днем недели
        self.LAST_LESSON_NUMBER = int(week_column_1.attrs['rowspan'])  # Получаем кол-во уроков

        week_column = rasp.find_all('td', {'style': ';text-align:left', 'rowspan': str(self.LAST_LESSON_NUMBER)})
        self.WORKING_DAYS_NUMBER = len(week_column)

        assert self.LAST_LESSON_NUMBER == len(lessons) // self.WORKING_DAYS_NUMBER

        table = []

        for day in range(self.WORKING_DAYS_NUMBER):
            table.append(lessons[day * self.LAST_LESSON_NUMBER:(day + 1) * self.LAST_LESSON_NUMBER])

        self.table = table

    def set_classes(self, ns_classes):
        for ns_class in ns_classes:
            self.classes.append(HTMLClass(ns_class.name))

    def get_class_by_name(self, name):
        for c in self.classes:
            if c.name == name:
                return c
        else:
            raise HTMLLoaderException

    def parse(self):
        for day_num, day_name in enumerate(self.DAYS):  # день (пн, вт и т.д.)
            for lesson_num in range(self.LAST_LESSON_NUMBER):  # номер урока
                lessons = self.table[day_num][lesson_num].contents
                if lesson_num == 0:  # если 1-ый урок, обрезаем столбец с названием дня недели и расписанием звонков
                    lessons = lessons[7::2]
                else:
                    lessons = lessons[5::2]  # убираем только расписание звонков

                for class_i, class_ in enumerate(self.classes):
                    lesson_block = lessons[class_i].contents
                    if lesson_block and type(lesson_block[0]) != NavigableString:
                        lesson_block, room_block = lesson_block[0].contents
                        groups_number = len(lesson_block.contents) // 2
                        for group_i in range(groups_number):
                            lesson_name = lesson_block.contents[group_i * 2].text.lstrip('/')
                            if not lesson_name:  # если в названии только "/"
                                for group_r in range(group_i - 1, -1, -1):
                                    lesson_name = lesson_block.contents[group_r * 2].text.lstrip('/')
                                    if lesson_name:
                                        break
                            lesson = HTMLLesson(name=lesson_name,
                                                teacher=lesson_block.contents[group_i * 2 + 1].text,
                                                room=room_block.text,
                                                day=self.DAYS[day_num],
                                                number=lesson_num)
                            self.classes[class_i].add_lesson(lesson)

    def get_subjects_set(self):
        for class_i, class_ in enumerate(self.classes):
            for lesson in class_.lessons:
                class_.add_subject(lesson.get_subject())
