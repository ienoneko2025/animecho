from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QMainWindow

from annotations import Annotations

class EditorWindow(QMainWindow):
  def __init__(self, annotations: Annotations, annotation_file_path: str, vid_url: QUrl):
    QMainWindow.__init__(self)
