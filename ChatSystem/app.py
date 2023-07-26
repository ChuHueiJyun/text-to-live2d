from flask import Flask, request
from flask_cors import CORS
from src.robot.robot import ChatGPT
from src.sentiment.sentiment import SentimentAnalysis
from service.speechService import SpeechService
from src.database.database import MongoDB

app = Flask(__name__)
CORS(app)
host = "http://localhost:8000"
users = {}
sentiment_analysis = SentimentAnalysis()
speechService = SpeechService()
mongoDB = MongoDB()

@app.route("/chat", methods=["POST"])
def getChat():
    data = request.json
    user = data["user"]
    msg = data["msg"]

    speechService.deleteSpeechByUser(user)

    if user not in users.keys():
        users[user] = ChatGPT()

    reply = users[user].chat(msg)
    sentence = users[user].splitMessage(reply)    
    speechService.text2Speech(user, "me", msg, 0)
    me = sentiment_analysis.textAnalysis(msg)
    robot = []

    for i in range(len(sentence)):
        speechService.text2Speech(user, "reply", sentence[i], i)
        robot.append({"sentence": sentence[i], "emotion": sentiment_analysis.textAnalysis(sentence[i]), "speech": f"{host}/static/speech/{user}/reply_{i}.mp3"})
    
    # time.sleep(10)
    return {"me" : {"sentence": msg, "emotion": me, "speech" : f"{host}/static/speech/{user}/me_0.mp3"}, "robot": robot}


@app.route("/story", methods=["POST"])
def getStory():
    data = request.json
    user = data["user"]
    msg = data["story"]
    type = data["type"]

    speechService.deleteSpeechByUser(user)

    if user not in users.keys():
        users[user] = ChatGPT()

    # reply = users[user].chat(msg)
    reply=""
    # story = users[user].story(msg)
    story = users[user].story(msg, type)    
    

    for page in story.keys():
        for sentence in range(len(story[page])):
            emotion = sentiment_analysis.textAnalysis(story[page][sentence]["content"])
            speechService.text2Speech(user, f"story_{page}", story[page][sentence]["content"], sentence)
            story[page][sentence]["emotion"] = emotion
            story[page][sentence]["speech"] = f"{host}/static/speech/{user}/story_{page}_{sentence}.mp3"
    
    return story

@app.route("/addUser", methods=["POST"])
def addUser():
    user = request.json
    mongoDB.addUser(user)

    return {"msg":"OK"}

@app.route("/login", methods=["POST"])
def login():
    user = request.json
    loginStatus = mongoDB.checkUser(user)

    return {"status": loginStatus}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)