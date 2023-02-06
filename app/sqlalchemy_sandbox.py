#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    Index('index_name', 'name') #indexes are used to speed up lookup on certain column values

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self): #instance method that determines their standard output value (i.e. what you see when you print() the object)
        return f"Student {self.id}: " \
            + f"{self.name}, "\
            + f"Grade {self.grade}"
    


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )
    
    ###### CREATE a single record 
    #session.add(albert_einstein) #generates a statement to include in the session's transaction

    # session.commit() #executes all statements in the transaction and saves any changes to the database
    # #also update your Student object with a id.

    ######## CREATE multiple records
    session.bulk_save_objects([albert_einstein, alan_turing]) 
    #to save multiple new records in a single line of code
    #does not associate the records with the session

    session.commit() #executes all statements in the transaction and saves any changes to the database
    #also update your Student object with a id.


    ###### READ single record
    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {alan_turing.id}.")


    ####### READ printing multiply bulk generated records w session query
    # #1
    # students = session.query(Student)
    # print([student for student in students])

    # #2
    # student = session.query(Student).all()
    # print(student)

    ####### READ selecting one columns
    # names = session.query(Student.name).all()
    # print(names)

    ####### READ ordering
    # students_by_name = session.query(
    #     Student.name).order_by(
    #     Student.name).all()
    
    # print(students_by_name)


    ###### READ descending order
    # students_by_grade_desc = session.query(
    #     Student.name, Student.grade).order_by(
    #     desc(Student.grade)).all()
    
    # print(students_by_grade_desc)

    # ###### READ limiting / oldest / youngest
    # oldest_student = session.query(
    #     Student.name, Student.birthday).order_by(
    #     desc(Student.grade)).limit(1).all()
    
    # print(oldest_student)

    # youngest_student = session.query(
    #     Student.name, Student.birthday).order_by(
    #     Student.grade).limit(1).all()
    
    # print(youngest_student)


    ####### READ first method 
    # youngest_student = session.query(
    #     Student.name, Student.birthday).order_by(
    #     Student.grade).first()
    
    # print(youngest_student)

    # ###### READ func (import func from sqlalchemy to execute common SQL operations)
    # student_count = session.query(func.count(Student.id)).first()

    # print(student_count)

    # ##### READ Filter
    # query = session.query(Student).filter(
    #     Student.name.like('%Alan%'),
    #     # Student.grade ==11
    #     ).all()
    
    # for record in query:
    #     print


    # ####### UPDATING 
    # #modify objects directly and then commit those changes through the session.
    # for student in session.query(Student):
    #     student.grade += 1

    # session.commit()

    # print([(student.name, student.grade) for student in session.query(Student)])

    ######## UPDATING
    # session.query(Student).update({
    #     Student.grade: Student.grade + 3
    # })

    # print([(
    #     student.name,
    #     student.grade
    # ) for student in session.query(Student)])



    # #### DELETE 
    # query = session.query(
    #     Student).filter(
    #     Student.name == "Albert Einstein"
    #     )
    
    # albert_einstein = query.first()

    # session.delete(albert_einstein)
    # session.commit()

    # albert_einstein = query.first()

    # print(albert_einstein)


    # ###### DELETE
    # query = session.query(
    #     Student).filter(
    #         Student.name == "Albert Einstein")
    
    # query.delete()

    # albert_einstein = query.first()

    # print(albert_einstein)