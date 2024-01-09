from node import Node
import json
from identifier import Identifier

class Logoot():
  def __init__(self, state) -> None:
    self.delete_queue = []
    Node.compare = lambda a, b: a.compare(b)
    self.root = Node(Identifier(0, '', 0))
    self.root.set_empty(False)
    self.root.add_child(Node(Identifier(1, '', 0)))
    self.root.add_child(Node(Identifier(2**64, '', 0)))

    if state: self.set_state(state)

  def parse_id(id):
    return Identifier(id.int, id.site, id.clock)

  def are_position_equal(a, b):
    if (len(a) != len(b)): return False
    for i in range(len(a)):
      if a[i].compare(b[i]) != 0: return False
    return True

  def insert(self, position, value):
    position = [self.parse_id(id) for id in position]
    for i in range(len(self.delete_queue)):
      if self.are_position_equal(self.delete_queue[i], position):
        del self.delete_queue[i]
        return
    
    existing_node = self.root.get_child_by_path(position, False)
    if existing_node: return

    node = self.root.get_child_by_path(position, True)
    if node:
      node.value = value
      node.set_empty(False)

  def delete(self, position):
    position = [self.parse_id(id) for id in position]
    node = self.root.get_child_by_path(position, False)
    if node and not node.empty:
      node.set_empty(True)
      node.trim_empty()
    else:
      for pos in self.delete_queue:
        if self.are_position_equal(pos, position):
          return
        
      self.delete_queue.append(position)

  def set_state(self, state):
    parsed = json.loads(state)

    def parse_node(n, parent):
      node = Node(Logoot.parse_id(n.id), n.value)
      node.parent = parent
      node.children = [parse_node(child, node) for child in n.children]
      node.size = n.size
      node.empty = n. empty
      return node
    
    self.root = parse_node(parsed["root"], None)
    self.delete_queue = [Logoot.parse_id(id) for id in parsed["deleteQueue"]]

  def get_state(self):
    return json.dumps({"root": self.root, "deleteQueue": self.delete_queue}, default=lambda key, value: value if key != "parent" else None)

  def get_value(self):
    arr = []
    def fn(node):
      if not node.empty:
        arr.append(node.value)
    self.root.walk(fn)
    return ''.join(arr)