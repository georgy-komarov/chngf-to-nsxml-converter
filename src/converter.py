from bs4 import BeautifulSoup

from exceptions import *


class Day:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class Room:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class Subject:
    def __init__(self, id, name, abbr):
        self.id = id
        self.name = name
        self.abbr = abbr
        self.teachers = []

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def __str__(self):
        return self.name


class Teacher:
    def __init__(self, id, firstname, lastname, midname):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.midname = midname
        self.name = f'{lastname} {firstname[0]}. {midname[0]}.'

    def __str__(self):
        return self.name


class PlanLesson:
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


class Class:
    def __init__(self, id, name, boys, girls):
        self.id = id
        self.name = name.upper()
        self.grade, self.letter = int(self.name[:-1]), self.name[-1]
        self.boys = int(boys)
        self.girls = int(girls)
        self.students = self.boys + self.girls

        self.plan = []

    def add_lesson(self, lesson):
        self.plan.append(lesson)

    def __str__(self):
        return self.name


class NSParser:
    DAYS = [Day(i, d) for i, d in enumerate(['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'])]

    def __init__(self):
        self.rasp = None
        self.ns = None

        self.rooms = None
        self.teachers = None
        self.subjects = None
        self.plans = None

    def parse(self, filename):
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
            teachers.append(Teacher(teacher.attrs['tid'], teacher.attrs['firstname'], teacher.attrs['lastname'],
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
            rooms.append(Room(room.attrs['id'], room.attrs['name']))

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
            subjects.append(Subject(subject.attrs['sid'], subject.attrs['name'], subject.attrs['abbr']))

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
            class_ = Class(class_tag.attrs['id'], class_tag.attrs['name'], class_tag.attrs['boys'],
                           class_tag.attrs['girls'])

            lessons_tags = class_tag.contents[1::2]
            for lesson_tag in lessons_tags:
                lesson = PlanLesson(lesson_tag.attrs['id'], lesson_tag.attrs['name'])
                lesson.set_teacher(self.teachers, lesson_tag.attrs['tid'])
                lesson.set_subject(self.subjects, lesson_tag.attrs['sid'])
                class_.add_lesson(lesson)

            plans.append(class_)

        return plans

    def load_all(self):
        self.rooms = self.get_rooms()
        self.teachers = self.get_teachers()
        self.subjects = self.get_subjects()
        self.plans = self.get_plan()


class HTMLParser:
    def __init__(self):
        pass

    def parse_html(self, filename):
        with open(filename, encoding='windows-1251') as f:
            rasp = BeautifulSoup(f, 'lxml')

        table_ = list(rasp.find('tbody'))[::2][1:]
        table = []

        for day in range(6):
            table.append(table_[day * 8:(day + 1) * 8])

        self.rasp = table


if __name__ == '__main__':
    nsparser = NSParser()
    nsparser.parse('./../ExportCM_2week.nsxml')
    nsparser.load_all()
