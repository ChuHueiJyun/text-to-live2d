from src.speech.speech import Speech
import os
import shutil

class SpeechService:
    def __init__(self):
        self.speech = Speech()

    def text2Speech(self, user, name, msg, cnt):
        if not os.path.isdir(f"static/speech/{user}"):
            os.mkdir(f"static/speech/{user}")
        self.speech.text2Speech(user, name ,msg, cnt)

    def deleteSpeechByUser(self, user):
        if os.path.isdir(f"static/speech/{user}"):
            shutil.rmtree(f"static/speech/{user}")

