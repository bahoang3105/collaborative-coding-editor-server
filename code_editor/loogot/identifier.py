class Identifier():
  int: int
  site: str
  clock: int

  def __init__(self, int: int, site: str, clock: int) -> None:
    self.int = int
    self.site = site
    self.clock = clock

  def compare(self, other):
    if self.int > other.int:
      return 1
    elif self.int < other.int:
      return -1
    else:
      if self.site > other.site:
        return 1
      elif self.site < other.site:
        return -1
      else:
        if self.clock > other.clock:
          return 1
        elif self.clock < other.clock:
          return -1
        else:
          return 0