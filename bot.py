from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import dbmanage as db
import string
from unidecode import unidecode


class Bot:
    def __init__(self):
        self.GOODBYE = ["do zobaczenia", "do widzenia"]
        self.HELP = ["help", "pomocy", "pomoz"]
        self.SCHEDULE = ["grafik", "harmonogram", "kalendarz"]
        self.chatbot = ChatBot('Harold Fit', database_uri='sqlite:///fit.db')
        self.train()
        self.db_manager = db.DBManager()

    def train(self):
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        trainer.train("corpus.classes")
        trainer.train("corpus.greetings")
        trainer.train("corpus.goodbye")
        trainer.train("corpus.thank-you")

    def is_goodbye(self, request):
        if request in self.GOODBYE:
            return True
        for goodbye in self.GOODBYE:
            if request.__contains__(goodbye):
                return True
        return False

    def is_help(self, request):
        if request in self.HELP:
            return True
        for word in self.HELP:
            if request.__contains__(word):
                return True
        return False

    def is_schedule(self, request):
        if request in self.SCHEDULE:
            return True
        for word in self.SCHEDULE:
            if request.__contains__(word):
                return True
        return False

    def print_help(self):
        print("Nazywam się Harold Fit i mam przyjemność pomagać klientom z harmonogramem zajęć fitnesowych :)\n"
              "Między innymi mogę znaleźć zajęcia wybranego instruktora, w wybranym dniu, wybranego typu "
              "albo dopasować trening do Twoich wymagań ;)")

    def run(self):
        print("\nWitam! Jestem botem i nazywam się Harold Fit. Mam przyjemność pomagać klientom "
              "z harmonogramem zajęć fitnesowych :)\n"
              "Między innymi mogę znaleźć zajęcia wybranego instruktora, w wybranym dniu, wybranego typu "
              "albo dopasować trening do Twoich wymagań ;)\n"
              "Serdecznie zapraszam do dialogu!")
        running = True
        while running:
            request = unidecode(input("Powiedz coś: ").lower().translate(str.maketrans('', '', string.punctuation)))

            if self.is_goodbye(request):
                running = False

            response = True

            if self.is_help(request):
                self.print_help()
                response = False

            if self.is_schedule(request):
                self.db_manager.print_schedule()
                response = False

            if response and self.db_manager.check_days(request):
                response = False

            if response and self.db_manager.check_classes(request):
                response = False

            if response and self.db_manager.check_instructors(request):
                response = False

            if response and self.db_manager.check_descriptions(request):
                response = False

            if response:
                print(self.chatbot.get_response(request))

        self.db_manager.close_connection()
