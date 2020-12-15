import sqlite3
from unidecode import unidecode


class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('fit.db')
        self.c = self.conn.cursor()
        self.CLASSES_MAP = dict()      # unidecoded -> ununidecoded
        self.CLASSES_UNIDECODED = []
        self.INSTRUCTORS_MAP = {}   # unidecoded -> ununidecoded
        self.INSTRUCTORS_UNIDECODED = []
        self.DAYS_OF_WEEK_MAP = dict()  # unidecoded -> ununidecoded
        self.DAYS_OF_WEEK_UNIDECODED = []
        self.DESCRIPTIONS_MAP = {}  # unidecoded -> ununidecoded
        self.DESCRIPTIONS_UNIDECODED = []

        self.set_all_classes()
        self.set_all_instructors()
        self.set_days_of_week()
        self.set_all_descriptions()

    def set_all_classes(self):
        self.c.execute('SELECT name FROM classes')
        for fit in self.c.fetchall():
            unidecoded = unidecode(fit[0])
            self.CLASSES_UNIDECODED.append(unidecoded)
            self.CLASSES_MAP[unidecoded] = fit[0]

    def set_all_instructors(self):
        self.c.execute('SELECT DISTINCT instructor FROM classes')
        for fit in self.c.fetchall():
            instructor = fit[0].lower()
            instructor_unidecoded = unidecode(instructor)
            self.INSTRUCTORS_UNIDECODED.append(instructor_unidecoded)
            self.INSTRUCTORS_MAP[instructor_unidecoded] = instructor

    def set_days_of_week(self):
        days_of_week = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
        for day in days_of_week:
            unidecoded = unidecode(day)
            self.DAYS_OF_WEEK_UNIDECODED.append(unidecoded)
            self.DAYS_OF_WEEK_MAP[unidecoded] = day

    def set_all_descriptions(self):
        self.c.execute('SELECT DISTINCT description FROM classes')
        for fit in self.c.fetchall():
            description = fit[0].lower()
            unidecoded = unidecode(description)
            self.DESCRIPTIONS_UNIDECODED.append(unidecoded)
            self.DESCRIPTIONS_MAP[unidecoded] = description

    def check_days(self, request):
        for day in self.DAYS_OF_WEEK_UNIDECODED:
            if request.__contains__(day):
                self.c.execute('SELECT * FROM classes WHERE day=?', (self.DAYS_OF_WEEK_MAP[day],))
                output = ""
                for fit in self.c.fetchall():
                    output += f"{fit[2]}:00-{fit[2]}:50 {fit[0]}\n"
                print(output, end="")
                return True
        return False

    def check_classes(self, request):
        for training in self.CLASSES_UNIDECODED:
            if request.__contains__(training):
                self.c.execute('SELECT description FROM classes WHERE name=?', (self.CLASSES_MAP[training],))
                output = f"{training} to {self.c.fetchone()[0]}. Zajęcia odbywają się:\n"
                self.c.execute('SELECT * FROM classes WHERE name=?', (self.CLASSES_MAP[training],))
                for fit in self.c.fetchall():
                    output += f"{fit[2]}:00-{fit[2]}:50 {fit[1]}\n"
                print(output, end="")
                return True
        return False

    def check_instructors(self, request):
        for instructor in self.INSTRUCTORS_UNIDECODED:
            if request.__contains__(instructor):
                self.c.execute('SELECT * FROM classes WHERE instructor=?', (self.INSTRUCTORS_MAP[instructor],))
                output = ""
                for fit in self.c.fetchall():
                    output += f"{fit[2]}:00-{fit[2]}:50 {fit[1].ljust(15)} {fit[0].ljust(20)}\n"
                print(output, end="")
                return True
        return False

    def print_trainings_with_description(self, description):
        self.c.execute('SELECT * FROM classes WHERE description=?', (description,))
        output = ""
        for fit in self.c.fetchall():
            output += f"{fit[2]}:00-{fit[2]}:50 {fit[1].ljust(15)} {fit[0].ljust(20)} {fit[4]}\n"
        print(output, end="")

    def check_descriptions(self, request):
        founded = False
        for word in request.split():
            if word != 'trening' and word != 'zajecia' and len(word) > 2:
                for description in self.DESCRIPTIONS_UNIDECODED:
                    if description.__contains__(word):
                        self.print_trainings_with_description(self.DESCRIPTIONS_MAP[description])
                        founded = True
        return founded

    def print_schedule(self):
        self.c.execute('SELECT * FROM classes ORDER BY id')
        output = ""
        for fit in self.c.fetchall():
            output += f"{fit[2]}:00-{fit[2]}:50 {fit[1].ljust(15)} {fit[0].ljust(20)} {fit[3].ljust(20)} {fit[4]}\n"
        print(output, end="")

    def close_connection(self):
        self.conn.close()
