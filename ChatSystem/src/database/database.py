import pymongo

class MongoDB:
    def __init__(self):
        myClient = pymongo.MongoClient("mongodb://localhost:27017")
        db = myClient["chatSystem"]
        self.users = db["users"]

    def addUser(self, user):
        self.users.insert_one(user)
    
    def checkUser(self, user):
        userDoc = list(self.users.find(user))
        
        if len(userDoc) != 0:
            return True
        else:
            return False