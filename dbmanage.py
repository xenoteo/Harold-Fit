import sqlite3
from unidecode import unidecode


class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('fit.db')
        self.c = self.conn.cursor()
        self.CLASSES_MAP = {}       # unidecoded -> ununidecoded
        self.CLASSES_UNIDECODED = []
        self.INSTRUCTORS_MAP = {}   # unidecoded -> ununidecoded
        self.INSTRUCTORS_UNIDECODED = []
        self.DAYS_OF_WEEK_MAP = {}  # unidecoded -> ununidecoded
        self.DAYS_OF_WEEK_UNIDECODED = []
        self.DESCRIPTIONS_MAP = {}  # unidecoded -> ununidecoded
        self.DESCRIPTIONS_UNIDECODED = []

        self.set_all_classes()
        self.set_all_instructors()
        self.set_days_of_week()
        self.set_all_descriptions()

    def set_map_and_unidecoded(self, data, unidecoded, map):
        for row in data:
            item = row.lower()
            item_unidecoded = unidecode(item)
            unidecoded.append(item_unidecoded)
            map[item_unidecoded] = item

    def query_to_array(self, query):
        self.c.execute(query)
        result = []
        for row in self.c.fetchall():
            result.append(row[0])
        return result

    def set_all_classes(self):
        self.set_map_and_unidecoded(self.query_to_array('SELECT name FROM classes'),
                                    self.CLASSES_UNIDECODED,
                                    self.CLASSES_MAP)

    def set_all_instructors(self):
        self.set_map_and_unidecoded(self.query_to_array('SELECT DISTINCT instructor FROM classes'),
                                    self.INSTRUCTORS_UNIDECODED,
                                    self.INSTRUCTORS_MAP)

    def set_days_of_week(self):
        days_of_week = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
        self.set_map_and_unidecoded(days_of_week, self.DAYS_OF_WEEK_UNIDECODED, self.DAYS_OF_WEEK_MAP)

    def set_all_descriptions(self):
        self.set_map_and_unidecoded(self.query_to_array('SELECT DISTINCT description FROM classes'),
                                    self.DESCRIPTIONS_UNIDECODED,
                                    self.DESCRIPTIONS_MAP)

    def print_fetched_data(self, data, output=""):
        for row in data:
            output += f"{row[2]}:00-{row[2]}:50 {row[1].ljust(15)} {row[0].ljust(20)} {row[3].ljust(20)} {row[4]}\n"
        print(output, end="")

    def check_days(self, request):
        for day in self.DAYS_OF_WEEK_UNIDECODED:
            if request.__contains__(day):
                self.c.execute('SELECT * FROM classes WHERE day=?', (self.DAYS_OF_WEEK_MAP[day],))
                self.print_fetched_data(self.c.fetchall())
                return True
        return False

    def check_classes(self, request):
        for training in self.CLASSES_UNIDECODED:
            if request.__contains__(training):
                self.c.execute('SELECT description FROM classes WHERE name=?', (self.CLASSES_MAP[training],))
                output = f"{training.capitalize()} to {self.c.fetchone()[0]}. Zajęcia odbywają się:\n"
                self.c.execute('SELECT * FROM classes WHERE name=?', (self.CLASSES_MAP[training],))
                self.print_fetched_data(self.c.fetchall(), output)
                return True
        return False

    def check_instructors(self, request):
        for instructor in self.INSTRUCTORS_UNIDECODED:
            if request.__contains__(instructor):
                self.c.execute('SELECT * FROM classes WHERE instructor=?', (self.INSTRUCTORS_MAP[instructor],))
                self.print_fetched_data(self.c.fetchall())
                return True
        return False

    def check_descriptions(self, request):
        founded = False
        for word in request.split():
            if word != 'trening' and word != 'zajecia' and len(word) > 2:
                for description in self.DESCRIPTIONS_UNIDECODED:
                    if description.__contains__(word):
                        self.c.execute('SELECT * FROM classes WHERE description=?',
                                       (self.DESCRIPTIONS_MAP[description],))
                        self.print_fetched_data(self.c.fetchall())
                        founded = True
        return founded

    def print_schedule(self):
        self.c.execute('SELECT * FROM classes ORDER BY id')
        self.print_fetched_data(self.c.fetchall())

    def close_connection(self):
        self.conn.close()
