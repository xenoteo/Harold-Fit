import sqlite3


class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('fit.db')
        self.c = self.conn.cursor()
        self.CLASSES = self.get_all_classes()
        self.INSTRUCTORS = self.get_all_instructors()
        self.DAYS_OF_WEEK = ["poniedziałek"]

    def get_all_classes(self):
        self.c.execute('SELECT name FROM classes')
        classes = []
        for fit in self.c.fetchall():
            classes.append(fit[0])
        return classes

    def get_all_instructors(self):
        self.c.execute('SELECT DISTINCT instructor FROM classes')
        instructors = []
        for fit in self.c.fetchall():
            instructors.append(fit[0].lower())
        return instructors

    def check_days(self, request):
        for day in self.DAYS_OF_WEEK:
            if request.__contains__(day):
                self.c.execute('SELECT * FROM classes WHERE day=?', (day,))
                output = ""
                for fit in self.c.fetchall():
                    output += f"{fit[2]}:00-{fit[2]}:50 {fit[0]}\n"
                print(output, end="")
                return True
        return False

    def check_classes(self, request):
        for training in self.CLASSES:
            if request.__contains__(training):
                self.c.execute('SELECT description FROM classes WHERE name=?', (training,))
                print(self.c.fetchone()[0])
                return True
        return False

    def check_instructors(self, request):
        for instructor in self.INSTRUCTORS:
            if request.__contains__(instructor):
                self.c.execute('SELECT * FROM classes WHERE instructor=?', (instructor,))
                output = ""
                for fit in self.c.fetchall():
                    output += f"{fit[2]}:00-{fit[2]}:50 {fit[1]} {fit[0]}\n"
                print(output, end="")
                return True
        return False

    def close_connection(self):
        self.conn.close()
