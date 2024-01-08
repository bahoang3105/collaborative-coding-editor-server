from threading import Lock
from channels.db import database_sync_to_async

from utils.IntervalTimer import IntervalTimer
from .models import Editor

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
  _online_editors = dict()

  async def add_user_to_editor(self, user, editor_id):
    if editor_id not in self._online_editors:
      await self._wakeup_editor(editor_id)
    if user["id"] not in self._online_editors[editor_id]["users"]:
      self._online_editors[editor_id]["users"].update({user["id"]: user})
    return

  def remove_user_from_editor(self, user, editor_id):
    if (editor_id not in self._online_editors) or (user["id"] not in self._online_editors[editor_id]["users"]):
      return
    self._online_editors[editor_id]["users"].pop(user["id"])
    if len(self._online_editors[editor_id]["users"]) == 0:
      self._online_editors[editor_id]["interval_save_data"].stop()
      self._save_editor_data(editor_id)
      self._online_editors.pop(editor_id)
    return

  async def _wakeup_editor(self, editor_id):
    editor = await self.get_editor_by_id(editor_id)
    self._online_editors.update({
      editor_id: {
        "users": dict(), 
        "content": editor.content, 
        "interval_save_data": IntervalTimer(60, self._save_editor_data, editor_id) 
      }
    })

  def _get_editor_data(self, editor_id):
    if editor_id not in self._online_editors:
      return
    return {
      "users": self._online_editors[editor_id]["users"],
      "content": self._online_editors[editor_id]["content"],
    }

  async def _save_editor_data(self, editor_id):
    if editor_id not in self._online_editors:
      return
    content = self._online_editors[editor_id]["content"]
    editor = await self.get_editor_by_id(editor_id)
    editor.content = content
    await database_sync_to_async(editor.save)()

  @database_sync_to_async
  def get_editor_by_id(self, editor_id):
    return Editor.objects.get(id=editor_id)
