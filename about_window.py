from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QStyle, QWidget

from ui_about_window import Ui_AboutWindow

class AboutWindow(QDialog):
  def __init__(self, parent: QWidget):
    QDialog.__init__(self, parent)

    self.__ui = Ui_AboutWindow()
    self.__ui.setupUi(self)

    self.__ui.btnOk.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton))
    self.__ui.btnOk.clicked.connect(self.__do_accept_terms)
    self.__ui.btnOk.setFocus()

  @Slot()
  def __do_accept_terms(self):
    self.accept()
