from django.db import models
from uuid import uuid4
import base64

def generateRandomString():
  return base64.b64encode(uuid4().bytes).replace('=', '')

# Create your models here.
class Editor(models.Model):
  id = models.CharField(max_length=200, default=generateRandomString(), primary_key=True)
  content = models.JSONField(empty_strings_allowed=True)

class WhiteBoard(models.Model):
  editor = models.ForeignKey(Editor, on_delete=models.CASCADE)
  content: models.JSONField
