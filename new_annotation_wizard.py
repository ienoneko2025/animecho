from traceback import print_exc

from PySide6.QtCore import QUrl, QEventLoop, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox, QStyle, QWidget

from ui_new_annotation_wizard import Ui_NewAnnotationWizard

from annotations import Annotations
from editor_window import EditorWindow
from user_preferences import UserPreferences

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
    save_location = self.__ui.fieldSaveLocationUrl.text()

    if save_location == '':
      QMessageBox.warning(self, '', 'Please select a save location')
      return

    vid_path = self.__ui.fieldVidFileUrl.text()

    if vid_path == '':
      QMessageBox.warning(self, '', 'Please select a video file')
      return

    editor = EditorWindow(Annotations(), save_location, QUrl.fromLocalFile(vid_path))
    editor.show()

    pref = UserPreferences()
    pref.last_vid_path = vid_path
    try:
      pref.save(f'{save_location}.user')
    except OSError:
      print_exc()

    self.close()

    QEventLoop().exec()
