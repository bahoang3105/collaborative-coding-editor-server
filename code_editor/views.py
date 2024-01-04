from uuid import uuid4;
from django.http import JsonResponse

def get_user_id(request):
  return JsonResponse({'userId': uuid4().hex})