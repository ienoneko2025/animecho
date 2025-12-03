#!/usr/bin/env python

from sys import exit, stderr, version_info

if version_info < (3, 12):
  print('Python too old', file=stderr)
  exit(1)

from argparse import ArgumentParser
import configparser
from os.path import exists
from re import match
from traceback import print_exc

from PySide6.QtCore import qVersion, QUrl
from PySide6.QtWidgets import QApplication

from annotations import Annotations, AnnotationParseError
from editor_window import EditorWindow
from loader_dlg import LoaderDialog
from player_window import PlayerWindow
from user_preferences import UserPreferences

def _assert_qt_ver():
  vs = qVersion()
  m = match(r'(\d+)\.(\d+)\.\d+', vs)
  if m is None:
    print('Cannot determine Qt version', file=stderr)
    exit(1)

  vt = tuple(map(int, m.groups()))
  if vt < (6, 5):
    print('Update your Qt installation', file=stderr)
    exit(1)

def _main():
  _assert_qt_ver()

  app = QApplication([])
  app.setApplicationName('animecho')

  ap = ArgumentParser()
  ap.add_argument('ANNOTATION_FILE', nargs='?')
  ap.add_argument('-video')
  ap.add_argument('-editor', action='store_true')
  args = ap.parse_args()

  if args.ANNOTATION_FILE is None:
    if args.video is not None:
      ap.error('Specify an annotation file')

    dlg = LoaderDialog()

    if args.editor:
      dlg.setProgramMode(LoaderDialog.ProgramMode.EDITOR)

    dlg.show()
  else:
    try:
      annotation = Annotations.load(args.ANNOTATION_FILE)
    except AnnotationParseError:
      print_exc()
      ap.error('Invalid annotation file')
    except OSError as exc:
      ap.error(f'Unable to open annotation file: {exc.strerror}')
    else:
      pref = UserPreferences()

      user_file_path = f'{args.ANNOTATION_FILE}.user'
      if exists(user_file_path):
        try:
          pref = UserPreferences.load(user_file_path)
        except configparser.Error:
          print_exc()
        except OSError:
          print_exc()

      vid_path = args.video

      if vid_path is None:
        if pref.last_vid_path is not None and exists(pref.last_vid_path):
          vid_path = pref.last_vid_path
        else:
          ap.error('Please specify a video file')

      vid_url = QUrl.fromLocalFile(vid_path)

      if args.editor:
        editor = EditorWindow(annotation, args.ANNOTATION_FILE, vid_url)
        editor.show()
      else:
        player = PlayerWindow(annotation, vid_url)
        player.show()

      pref.last_vid_path = vid_path

      # XXX: config is always saved even if the video didn't play
      #      e.g. the video file is not accessible

      try:
        pref.save(user_file_path)
      except OSError:
        print_exc()

  app.exec()

_main()
