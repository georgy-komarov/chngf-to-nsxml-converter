from bs4 import BeautifulSoup
from bs4 import Tag

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
        self.name = f'{lastname} {firstname[0]}. {midname[0]}.'

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
class HTMLSubject:
    def __init__(self, name, teacher, room=None):
        self.name = name
        self.teacher = teacher
        self.room = room


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

    def parse_all(self):
        self.rooms = self.get_rooms()
        self.teachers = self.get_teachers()
        self.subjects = self.get_subjects()
        self.plans = self.get_plan()


class HTMLParser(TimetableConverter):
    def __init__(self):
        self.table = None

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


if __name__ == '__main__':
    nsparser = NSParser()
    nsparser.load('./../ExportCM_2week.nsxml')
    nsparser.parse_all()

    htmlparser = HTMLParser()
    htmlparser.load('./../7raw.html')
    htmlparser.get_subjects_set()
