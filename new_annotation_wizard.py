from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox, QStyle, QWidget

from ui_new_annotation_wizard import Ui_NewAnnotationWizard

class NewAnnotationWizard(QWidget):
  def __init__(self):
    QWidget.__init__(self)

    self.__ui = Ui_NewAnnotationWizard()
    self.__ui.setupUi(self)

    self.__ui.btnOK.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton))

    self.__ui.btnPickSaveLocation.clicked.connect(self.__do_pick_save_location)
    self.__ui.btnPickVidFile.clicked.connect(self.__do_pick_vid_file)
    self.__ui.btnOK.clicked.connect(self.__do_jump_to_editor)

  @Slot()
  def __do_pick_save_location(self):
    path, _ = QFileDialog.getSaveFileName(self, filter='Annotation Files (*.annotations)')
    if path == '':
      return

    if not path.endswith('.annotations'):
      path = f'{path}.annotations'

    self.__ui.fieldSaveLocationUrl.setText(path)

  @Slot()
  def __do_pick_vid_file(self):
    path, _ = QFileDialog.getOpenFileName(self, filter='Video Files (*.mp4 *.mkv)')
    if path != '':
      self.__ui.fieldVidFileUrl.setText(path)

  @Slot()
  def __do_jump_to_editor(self):
    if self.__ui.fieldSaveLocationUrl.text() == '':
      QMessageBox.warning(self, '', 'Please select a save location')
      return

    if self.__ui.fieldVidFileUrl.text() == '':
      QMessageBox.warning(self, '', 'Please select a video file')
      return
