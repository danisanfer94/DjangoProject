from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
from datetime import datetime

class Monguito:

    def __init__(self):
        connect=MongoClient("localhost",27017)
        db=connect.PythonProject
        self.collection=db.Usuaris
        self.failcollection=db.FailLogin

    def userExists(self,nomusuari):
        if self.collection.find({'username':nomusuari}).count() > 0 :
            return True
        else:
            return False

    def mostrarUsers(self):
        return self.collection.find({},{'_id':False})

    def hashPass(self,password):
        return pbkdf2_sha256.hash(password)

    def checkPass(self,nom,passw):
        usuari = self.collection.find_one({'username':nom})
        return pbkdf2_sha256.verify(passw,usuari['password'])

    def insertUser(self,user):
        self.collection.insert_one(user.__dict__)
        return True

    def incLogin(self,nomusuari):
        self.collection.update_one({'username':nomusuari},{'$inc':{'logins':1}})
        return True

    def fail(self,nom,passw):
        time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.failcollection.insert_one({'username':nom,'password':passw,'datetime':time})

    def delUser(self,nom):
        self.collection.delete_one({'username':nom})
        return True

    def findFails(self):
        return self.failcollection.find({},{'_id':False})

    def dropFails(self):
        self.failcollection.delete_many({})
