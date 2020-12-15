import os
import shutil


"""Removing unnecessary files"""

try:
    os.remove("db.sqlite3")
    os.remove("sentence_tokenizer.pickle")
    shutil.rmtree("__pycache__")
    print("Successfully cleaned.")
except FileNotFoundError:
    print("Already cleaned.")
