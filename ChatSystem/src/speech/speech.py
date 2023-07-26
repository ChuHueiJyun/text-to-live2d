
import pyttsx3

class Speech:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty("voices")
        # for voice in voices:
        #     print(voice.id)
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 120)

    def text2Speech(self, user, name, text, cnt):
        self.engine.save_to_file(text , f"static/speech/{user}/{name}_{cnt}.mp3")
        self.engine.runAndWait()


