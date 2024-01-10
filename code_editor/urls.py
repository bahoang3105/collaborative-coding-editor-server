from django.urls import path

from . import views

app_name= "code_editor"
urlpatterns = [
  path("create/", views.create_editor, name="create_editor"),
]