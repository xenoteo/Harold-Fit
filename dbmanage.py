import sqlite3
from unidecode import unidecode


class DBManager:
    """ Class responsible for communication with a database. """

    def __init__(self):
        self.conn = sqlite3.connect('fit.db')
        self.c = self.conn.cursor()
        self.CLASSES_MAP = {}       # unidecoded -> not unidecoded (with polish letters)
        self.CLASSES_UNIDECODED = []        # array of all the classes (without polish letters)
        self.INSTRUCTORS_MAP = {}   # unidecoded -> not unidecoded (with polish letters)
        self.INSTRUCTORS_UNIDECODED = []    # array of all the instructors (without polish letters)
        self.DAYS_OF_WEEK_MAP = {}  # unidecoded -> not unidecoded (with polish letters)
        self.DAYS_OF_WEEK_UNIDECODED = []   # array of all the days of week (without polish letters)
        self.DESCRIPTIONS_MAP = {}  # unidecoded -> not unidecoded (with polish letters)
        self.DESCRIPTIONS_UNIDECODED = []   # array of all the descriptions (without polish letters)

        self.set_all_classes()
        self.set_all_instructors()
        self.set_days_of_week()
        self.set_all_descriptions()

    def set_map_and_unidecoded(self, data, unidecoded, unicode_map):
        """
        A function setting unidecoded array based on a normal array
        as well as setting unidecoded -> not unidecoded map.
        :param data: an unchanged input array
        :param unidecoded: an array to write unidecoded input array
        :param unicode_map: a map to set unidecoded -> not unidecoded relationship
        """

        for row in data:
            item = row.lower()
            item_unidecoded = unidecode(item)
            unidecoded.append(item_unidecoded)
            unicode_map[item_unidecoded] = item

    def query_to_array(self, query):
        """
        A function executing provided query and writing its output to an array.
        :param query: a query to execute
        :return an array containing result after executing the query
        """

        self.c.execute(query)
        result = []
        for row in self.c.fetchall():
            result.append(row[0])
        return result

    def set_all_classes(self):
        """ A function setting CLASSES_UNIDECODED and CLASSES_MAP, after getting all the classes from the database. """

        self.set_map_and_unidecoded(self.query_to_array('SELECT name FROM classes'),
                                    self.CLASSES_UNIDECODED,
                                    self.CLASSES_MAP)

    def set_all_instructors(self):
        """
        A function setting INSTRUCTORS_UNIDECODED and INSTRUCTORS_MAP,
        after getting all the instructors from the database.
        """

        self.set_map_and_unidecoded(self.query_to_array('SELECT DISTINCT instructor FROM classes'),
                                    self.INSTRUCTORS_UNIDECODED,
                                    self.INSTRUCTORS_MAP)

    def set_days_of_week(self):
        """ A function setting DAYS_OF_WEEK_UNIDECODED and DAYS_OF_WEEK_MAP. """

        days_of_week = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
        self.set_map_and_unidecoded(days_of_week, self.DAYS_OF_WEEK_UNIDECODED, self.DAYS_OF_WEEK_MAP)

    def set_all_descriptions(self):
        """
        A function setting DESCRIPTIONS_UNIDECODED and DESCRIPTIONS_MAP,
        after getting all the descriptions from the database.
        """

        self.set_map_and_unidecoded(self.query_to_array('SELECT DISTINCT description FROM classes'),
                                    self.DESCRIPTIONS_UNIDECODED,
                                    self.DESCRIPTIONS_MAP)

    def print_fetched_data(self, data, output=""):
        """
        A function printing formatted fetched data.
        :param data: data to be printed
        :param output: output to be filled with provided data
        """

        for row in data:
            output += f"{row[2]}:00-{row[2]}:50 {row[1].ljust(15)} {row[0].ljust(20)} {row[3].ljust(20)} {row[4]}\n"
        print(output, end="")

    def check_days(self, request):
        """
        A function that checks whether input contain request about certain day of week,
        and if so gets all the necessary data from the database and prints it.
        :param request: request to be analysed
        :return: whether input contain request about any day of week
        """

        for day in self.DAYS_OF_WEEK_UNIDECODED:
            if request.__contains__(day):
                self.c.execute('SELECT * FROM classes WHERE day=?', (self.DAYS_OF_WEEK_MAP[day],))
                self.print_fetched_data(self.c.fetchall())
                return True
        return False

    def check_classes(self, request):
        """
        A function that checks whether input contain request about certain class,
        and if so gets all the necessary data from the database and prints it.
        :param request: request to be analysed
        :return: whether input contain request about any class
        """

        for training in self.CLASSES_UNIDECODED:
            if request.__contains__(training):
                self.c.execute('SELECT description FROM classes WHERE name=?', (self.CLASSES_MAP[training],))
                output = f"{training.capitalize()} to {self.c.fetchone()[0]}. Zajęcia odbywają się:\n"
                self.c.execute('SELECT * FROM classes WHERE name=?', (self.CLASSES_MAP[training],))
                self.print_fetched_data(self.c.fetchall(), output)
                return True
        return False

    def check_instructors(self, request):
        """
        A function that checks whether input contain request about certain instructor,
        and if so gets all the necessary data from the database and prints it.
        :param request: request to be analysed
        :return: whether input contain request about any instructor
        """

        for instructor in self.INSTRUCTORS_UNIDECODED:
            if request.__contains__(instructor):
                self.c.execute('SELECT * FROM classes WHERE instructor=?', (self.INSTRUCTORS_MAP[instructor],))
                self.print_fetched_data(self.c.fetchall())
                return True
        return False

    def check_descriptions(self, request):
        """
        A function that checks whether input contain request about certain class description,
        and if so gets all the necessary data from the database and prints it.
        :param request: request to be analysed
        :return: whether input contain request about any class description
        """

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
        """ A function getting all the schedule from the database and printing it. """

        self.c.execute('SELECT * FROM classes ORDER BY id')
        self.print_fetched_data(self.c.fetchall())

    def close_connection(self):
        """ A function closing a connection with the database. """

        self.conn.close()
