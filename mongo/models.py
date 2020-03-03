from django.db import models


# Create your models here.
class User:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.logins=0
