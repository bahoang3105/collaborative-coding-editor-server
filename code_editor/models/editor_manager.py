from threading import Lock
from .. import models

class SingletonMeta(type):
  _instances = {}
  _lock: Lock = Lock()

  def __call__(cls, *args, **kwargs):
    with cls._lock:
      if cls not in cls._instances:
        instance = super().__call__(*args, **kwargs)
        cls._instances[cls] = instance
    return cls._instances[cls]
  
class EditorManager(metaclass=SingletonMeta):
  online_editors = dict()

  def add_user_to_editor(self, user, editor_id):
    if (editor_id not in self.online_editors):
      self.wakeup_editor(editor_id)

  def remove_user_from_editor(self, user, editor_id):
    if ((editor_id not in self.online_editors) or (user not in self.online_editors[editor_id])):
      return
    

  def wakeup_editor(self, editor_id):
    editor = models.Editor.objects.get(id=editor_id)
    self.online_editors.update({[editor_id]: {"users": [], "content": editor.content, "interval_save_data": 1 }})

  def get_editor_data(self, editor_id):
    return

  def save_editor_data(self, editor_id):
    return