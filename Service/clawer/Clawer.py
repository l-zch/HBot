from typing import List, Dict
from Service.Label import Label


class Clawer:

  def get_repository_index(self) -> str:
    pass

  def get_labels(self) -> List[Label]:
    pass
  
  def get_title(self) -> str:
    pass

  def get_labels_map(self) -> Dict[str, List[Label]]:
    pass

  def get_pages(self) -> int:
    pass