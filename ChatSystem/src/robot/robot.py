import openai
import nltk
import json

class storyFactory:
    def __init__(self, msg, file_type):
        self.msg = msg
        self.file_type = file_type
        
    def createStory(self):
        if self.file_type == 'txt':
            txt = txt2story(self.msg)
            return txt
        elif self.file_type == 'json':
            json = json2story(self.msg)
            return json


class txt2story:
    def __init__(self, msg):
        self.msg = msg

    def process(self):  
        sentence = self.msg.split('\n')
        story = {}
        page = 0

        for data in sentence:
            if data[:4] == "Page" or data[:4] == "page":
                page += 1
                story[page] = []
            elif data == "":
                pass
            else:
                story[page].append({"content": data})
        return story

class json2story:
    def __init__(self, msg):
        self.msg = msg

    def process(self):
        sentences = json.loads(self.msg)
        story = {}
        page = 1

        for data in sentences.values():
            story[page] = []
            sentence = data.split("\n")

            for line in sentence:
                story[page].append({"content": line})
            
            page += 1
        return story

class ChatGPT:
    def __init__(self):
        openai.api_key = open("src/robot/key.txt", "r").read().strip("\n")
        self.message_history = []
        nltk.download('punkt')
    
    def chat(self, msg):
        self.message_history.append({"role": "user", "content": f"{msg}"})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message_history
        )
        reply_content = completion.choices[0].message.content
        self.message_history.append({"role": "assistant", "content": f"{reply_content}"})
        return reply_content

    @staticmethod
    def splitMessage(msg):
        sentence = nltk.sent_tokenize(msg)
        return sentence

    @staticmethod
    def story(msg, file_type):
        story_factory = storyFactory(msg, file_type)
        story_parser = story_factory.createStory()
        story = story_parser.process()

        return story