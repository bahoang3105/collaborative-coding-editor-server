from django.db import models

from utils.String import generateRandomString

def defaultJson():
  return {}

# Create your models here.
class Editor(models.Model):
  id = models.CharField(max_length=200, default=generateRandomString(), primary_key=True)
  content = models.JSONField(default=defaultJson)

class WhiteBoard(models.Model):
  editor = models.ForeignKey(Editor, on_delete=models.CASCADE)
  content: models.JSONField(default=defaultJson)
