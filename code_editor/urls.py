from django.urls import path

import views

app_name= "code_editor"
urlpatterns = [
  path("room/", views.create_editor, name="create_editor"),
]