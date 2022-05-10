from typing import List

from utils.assets import Repository



class ContentManager:

  def __init__(self, pages, repository_url:str, indexes: List[str]):
    self.pages = pages
    self.repository_url = repository_url
    self.indexes = indexes

  def next(self):
    self.page += 1
    return self.refresh()

  def previous(self):
    self.page -= 1
    return self.refresh()

  def refresh(self):
    if(self.page <= 0 or self.page > self.pages):
      return None
    return self.repository_url.format(self.indexes[self.page])