from sqlalchemy import func, desc, select, and_

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def help():
    print(
    '''1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    2. Знайти студента із найвищим середнім балом з певного предмета.
    3. Знайти середній бал у групах з певного предмета.
    4. Знайти середній бал на потоці (по всій таблиці оцінок).
    5. Знайти які курси читає певний викладач.
    6. Знайти список студентів у певній групі.
    7. Знайти оцінки студентів у окремій групі з певного предмета.
    8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
    9. Знайти список курсів, які відвідує студент.
    10. Список курсів, які певному студенту читає певний викладач.
    11. Середній бал, який певний викладач ставить певному студентові.
    12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
    
    Стандартний вигляд команди: "Номер команди" "опціональний аргумент 1" "опціональний аргумент 2" '''
          )


def select_1():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result


def select_2(discipline_id: int):
    r = session.query(Discipline.name,
                      Student.fullname,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()
    return r


def select_3(discipline_id):
    r = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Discipline).join(Student).join(Group)\
        .filter(Discipline.id == discipline_id).group_by(Group.name).all()
    return r


def select_4():
    r = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')).select_from(Grade).all()
    return r


def select_5(teacher_id):
    r = session.query(Discipline.name).select_from(Discipline).join(Teacher).filter(Teacher.id == teacher_id).all()
    return r


def select_6(group_id):
    r = session.query(Student.fullname).select_from(Student).join(Group).filter(Group.id == group_id).all()
    return r


def select_7(group_id, discipline_id):
    r = session.query(Student.fullname, Grade.grade)\
        .select_from(Grade).join(Discipline).join(Student).join(Group)\
        .filter(and_(Group.id == group_id, Discipline.id == discipline_id))\
        .group_by(Student.fullname, Grade.grade)\
        .order_by(Student.fullname).all()
    return r


def select_8(teacher_id):
    r = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Discipline).join(Teacher)\
        .filter(Teacher.id == teacher_id).all()
    return r


def select_9(student_id):
    r = session.query(Discipline.name)\
        .select_from(Grade).join(Discipline).join(Student)\
        .filter(Student.id == student_id).group_by(Discipline.name).all()
    return r


def select_10(student_id, teacher_id):
    r = session.query(Discipline.name)\
        .select_from(Grade).join(Discipline).join(Teacher).join(Student)\
        .filter(and_(Student.id == student_id, Teacher.id == teacher_id))\
        .group_by(Discipline.name).all()
    return r


def select_11(teacher_id, student_id):
    r = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Discipline).join(Teacher).join(Student)\
        .filter(and_(Student.id == student_id, Teacher.id == teacher_id))\
        .all()
    return r


def select_12(discipline_id, group_id):
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())

    r = session.query(Discipline.name,
                      Student.fullname,
                      Group.name,
                      Grade.date_of,
                      Grade.grade
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group)\
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery)) \
        .order_by(desc(Grade.date_of)) \
        .all()
    return r


commands = {
    '1': select_1,
    '2': select_2,
    '3': select_3,
    '4': select_4,
    '5': select_5,
    '6': select_6,
    '7': select_7,
    '8': select_8,
    '9': select_9,
    '10': select_10,
    '11': select_11,
    '12': select_12,
}


def main():
    while True:
        command = input('Enter command: ')
        command_list = command.split()
        if command_list[0] in ['3', '5', '6', '8', '9']:
            print(commands[command_list[0]](command_list[1]))

        elif command_list[0] in ['7', '10', '11', '12']:
            print(commands[command_list[0]](command_list[1], command_list[2]))

        elif command_list[0] == 'help':
            help()

        elif command_list[0] == "exit":
            exit()

        else:
            print(commands[command_list[0]]())


if __name__ == '__main__':
    main()
