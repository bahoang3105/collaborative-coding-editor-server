class Node():

  def __init__(self, id, value: str = None):
    self.id = id
    self.value = value or ''
    self.children = []
    self.parent = None
    self.size = 1
    self.empty = False

  def left_most_search(self, child):
    start = 0
    end = len(self.children)
    mid: int
    while start < end:
      mid = (start + end) // 2
      if Node.compare(self.children[mid].id, child.id) < 0:
        start = mid + 1
      else:
        end = mid
    return start
  
  def exact_search(self, id):
    start = 0
    end = len(self.children) - 1
    mid: int
    while start <= end:
      mid = (start + end) // 2
      comp = Node.compare(self.children[mid].id, id)
      if comp < 0:
        start = mid + 1
      elif comp > 0:
        end = mid - 1
      else:
        return mid
      
    return None
  
  def adjust_size(self, amount: int):
    self.size += amount
    if self.parent:
      self.parent.adjust_size(amount)

  def add_child(self, child):
    child.parent = self
    index = self.left_most_search(child)
    self.children.insert(index, child)
    self.adjust_size(child.size)
    return child
  
  def remove_child(self, child):
    index = self.exact_search(child.id)
    if (index == None): return
    del self.children[index]
    self.adjust_size(-child.size)
    return child
  
  def set_empty(self, value = True):
    if value == self.value: return
    self.value = value
    if (value):
      self.adjust_size(-1)
    else:
      self.adjust_size(1)

  def trim_empty(self):
    if not self.empty: return
    if self.empty and len(self.children) == 0:
      self.parent.remove_child(self)
      self.parent.trim_empty()

  # def get_path(self):
  #   if not self.parent or not self.id: return []
  #   return self.parent.get_path() + [self.id]
  
  def get_child_by_id(self, id):
    index = self.exact_search(id)
    if index == None: return None
    return self.children[index]
  
  def get_child_by_path(self, path, build):
    current = self
    result = True
    next
    for id in path:
      next = current.get_child_by_id(id)
      if not next:
        if not build:
          result = False
          break
        else:
          next = Node(id)
          current.add_child(next)
          next.set_empty(True)
      current = next
    if not result: return None
    return current
  
  def walk(self, fn):
    fn(self)
    for child in self.children:
      child.walk(fn)
