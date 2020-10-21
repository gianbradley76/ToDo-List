import sys
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, date, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def task_today():
    print(f"Today {datetime.today().day} {datetime.today().strftime('%b')}:")
    today = datetime.today()
    rows = session.query(Task).filter(Task.deadline == today.date()).all()

    if rows is not None:
        i = 1
        for row in rows:
            print(f'{i}) {row.task}')
            i += 1
    else:
        print("Nothing to do today!")

    print()


def determine_weekday(weekday):
    day_name = ['Monday',
                'Tueday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday']
    return day_name[weekday]


def week_task():
    today = datetime.today().date()
    rows = session.query(Task).order_by(Task.deadline).all()
    tasks = session.query(Task).order_by(Task.deadline).all()

    for row in rows:
        if timedelta(days=0) <= row.deadline - today <= timedelta(days=7):
            print(f"{row.deadline.strftime('%b')} {row.deadline.day}")
            counter = 1
            for task in tasks:
                if task.deadline == row.deadline:
                    print(f'{counter}) {task.task}')
                    counter += 1
        print()
    # print(week_dates)
    '''for row in session.query(Task, Task.deadline):
        print(f"{row.deadline.strftime('%b')} {row.deadline.day}")
        # print(task)'''

    print()


def all_task():
    rows = session.query(Task).all()
    i = 1
    for row in rows:
        print(f"{i}) {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        i += 1
    print()


def add_task():
    print("Enter task")
    task_input = input()
    print("Enter deadline")
    date_entry = input()
    year, month, day = map(int, date_entry.split('-'))
    date1 = date(year, month, day)
    new_row = Task(task=task_input, deadline=date1)
    session.add(new_row)
    session.commit()

    print("The task has been added!")
    print()


def main():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Add task")
    print("0) Exit")
    menu_input = int(input())
    print()

    if menu_input == 1:
        task_today()
    elif menu_input == 2:
        week_task()
    elif menu_input == 3:
        all_task()
    elif menu_input == 4:
        add_task()
    elif menu_input == 0:
        print("Bye!")
        sys.exit(0)


if __name__ == '__main__':
    while True:
        main()

# Write your code here
# print("Today:")
# print("1) Do yoga")
# print("2) Make breakfast")
# print("3) Learn basics of SQL")
# print("4) Learn what is ORM")
