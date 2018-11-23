from threading import Lock
from datetime import datetime


class FileHandler:

    # def __init__(self):

    def access_text_file(self, file_path, usage=None):
        now = None
        if usage is None:
            text_file = open(file_path, 'a', encoding="utf-8")
            now = str(datetime.now().timestamp())
            return text_file, now
        text_file = open(file_path, 'r+', encoding="utf-8")
        return text_file, now