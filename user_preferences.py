from configparser import ConfigParser
from dataclasses import dataclass
from typing import Optional, Self

@dataclass
class UserPreferences:
  last_vid_path: Optional[str] = None

  @classmethod
  def __create_configparser(cls):
    parser = ConfigParser()

    # case-sensitive keys
    parser.optionxform = lambda optionstr: optionstr

    return parser

  @classmethod
  def load(cls, path: str) -> Self:
    pref = cls()

    with open(path, 'r', encoding='utf-8') as f:
      ini = cls.__create_configparser()
      ini.read_file(f)

      try:
        section = ini['Preferences']
      except KeyError:
        pass
      else:
        pref.last_vid_path = section.get('LastVideoPath')

    return pref

  def save(self, path: str):
    d = {}

    if self.last_vid_path is not None:
      d['LastVideoPath'] = self.last_vid_path

    ini = self.__create_configparser()
    ini['Preferences'] = d

    with open(path, 'w', encoding='utf-8') as f:
      ini.write(f)
