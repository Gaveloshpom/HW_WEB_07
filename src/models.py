from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from .db import Base

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)
    group_id = Column("group_id", ForeignKey("groups.id",ondelete="CASCADE"))
    group = relationship("Group", backref="students")


class Discipline(Base):
    __tablename__ = "disciplines"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    teacher_id = Column("teacher_id", ForeignKey("teachers.id", ondelete="CASCADE"))
    group = relationship("Teacher", backref="disciplines")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column("date_of", Date, nullable=True)
    student_id = Column(ForeignKey("students.id", ondelete="CASCADE"))
    disciplines_id = Column(ForeignKey("disciplines.id", ondelete="CASCADE"))
    student = relationship("Student", backref="grade")
    disciplines = relationship("Discipline", backref="grade")