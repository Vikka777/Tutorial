from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from database.db import engine as select_engine
Session = sessionmaker(bind=select_engine)

session = Session()

from my_project.database.models import Student, Grade, Discipline, Group, Teacher  # Імпорт моделей


#Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1(session):
    top_students = session.query(Student, func.avg(Grade.grade).label('average_score')) \
        .join(Grade) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.grade).desc()) \
        .limit(5) \
        .all()
    return top_students

#Знайти студента із найвищим середнім балом з певного предмета
def select_2(session, subject_name):
    top_student = session.query(Student, func.avg(Grade.grade).label('average_score')) \
        .join(Grade) \
        .filter(Grade.subject == subject_name) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.grade).desc()) \
        .first()
    return top_student

#Знайти середній бал у групах з певного предмета
def select_3(session, subject_name):
    avg_scores_by_group = session.query(Student.group_id, func.avg(Grade.grade).label('average_score')) \
        .join(Grade) \
        .filter(Grade.subject == subject_name) \
        .group_by(Student.group_id) \
        .all()
    return avg_scores_by_group


#Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4(session):
    average_score = session.query(func.avg(Grade.grade).label('average_score')).scalar()
    return average_score

# Запит 5: Знайти, які курси читає певний викладач
def select_5(session, teacher_name):
    courses_taught_by_teacher = session.query(Discipline.name).filter(Discipline.teacher.has(Teacher.fullname == teacher_name)).distinct().all()
    return courses_taught_by_teacher

# Запит 6: Знайти список студентів у певній групі
def select_6(session, group_name):
    students_in_group = session.query(Student).filter(Student.group.has(Group.name == group_name)).all()
    return students_in_group


# Запит 7: Знайти оцінки студентів в окремій групі з певного предмета
def select_7(session, group_name, subject_name):
    grades_in_group = session.query(Student, Grade).filter(Student.group.has(Group.name == group_name), Grade.subject == subject_name).all()
    return grades_in_group

#Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(session, teacher_name):
    avg_score_by_teacher = session.query(Discipline.teacher_id, func.avg(Grade.grade).label('average_score')) \
        .join(Grade) \
        .filter(Discipline.teacher.has(Teacher.fullname == teacher_name)) \
        .group_by(Discipline.teacher_id) \
        .all()
    return avg_score_by_teacher

#Знайти список курсів, які відвідує певний студент
def select_9(session, student_name):
    courses_taken_by_student = session.query(Grade.subject).join(Student) \
        .filter(Student.fullname == student_name) \
        .distinct().all()
    return courses_taken_by_student

#Список курсів, які певному студенту читає певний викладач
def select_10(session, student_name, teacher_name):
    courses_taught_to_student_by_teacher = session.query(Grade.subject) \
        .join(Student) \
        .join(Discipline) \
        .filter(Student.fullname == student_name, Discipline.teacher.has(Teacher.fullname == teacher_name)) \
        .distinct().all()
    return courses_taught_to_student_by_teacher