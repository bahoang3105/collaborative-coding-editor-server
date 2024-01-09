
from django.http import JsonResponse

from code_editor.loogot.logoot import Logoot
from models import Editor

def create_editor(request):
  content = Logoot().get_state()
  editor = Editor().objects.create(content=content)
  return JsonResponse({"editor_id": editor.id})