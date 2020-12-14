from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import dbmanage as db


class Bot:
    def __init__(self):
        self.goodbye = ["do zobaczenia", "do widzenia"]
        self.chatbot = ChatBot('Harold Fit')
        self.train()
        self.db_manager = db.DBManager()

    def train(self):
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        trainer.train("corpus.classes")
        trainer.train("corpus.greetings")
        trainer.train("corpus.goodbye")

    def run(self):
        running = True
        while running:
            request = input("Powiedz coś: ")
            request_lower = request.lower()
            if request_lower in self.goodbye:
                running = False

            response = True
            if self.db_manager.check_days(request_lower):
                response = False

            if self.db_manager.check_classes(request_lower):
                response = False

            if self.db_manager.check_instructors(request_lower):
                response = False

            if response:
                print(self.chatbot.get_response(request))

        self.db_manager.close_connection()
