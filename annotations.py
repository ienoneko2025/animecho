from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Self, Sequence, override

from time_serialization import format_time_str_from_ms

class AnnotationParseError(ValueError):
  pass

class TooManyOrFewFields(AnnotationParseError):
  pass

@dataclass
class Event(ABC):
  time_ms: int

  @classmethod
  @abstractmethod
  def get_tag_name(cls) -> str:
    pass

  @classmethod
  @abstractmethod
  def parse(cls, ev_time: int, fields: Sequence[str]) -> Self:
    pass

  @abstractmethod
  def fmt(self) -> tuple[str]:
    pass

@dataclass
class NullEvent(Event):
  @classmethod
  @override
  def get_tag_name(cls) -> str:
    raise AssertionError

  @classmethod
  @override
  def parse(cls, ev_time: int, fields: Sequence[str]) -> Self:
    raise AssertionError

  @override
  def fmt(self) -> tuple[str]:
    raise AssertionError

@dataclass
class DialogueEvent(Event):
  @classmethod
  @override
  def get_tag_name(cls) -> str:
    return 'dialogue'

  @classmethod
  @override
  def parse(cls, ev_time: int, fields: Sequence[str]) -> Self:
    if len(fields) != 0:
      raise TooManyOrFewFields

    return cls(ev_time)

  @override
  def fmt(self) -> tuple[str]:
    return ()

@dataclass
class EventList:
  inner: Event
  ll_prev: Optional[Self] = None
  ll_next: Optional[Self] = None

class Annotations:
  def __init__(self):
    self.__events = EventList(NullEvent(0))

  def get_events(self) -> EventList:
    return self.__events

  @classmethod
  def load(cls, path: str) -> Self:
    instance = cls()

    with open(path, 'r', encoding='utf-8') as f:
      pass

    return instance

  def save(self, path: str):
    with open(path, 'w', encoding='utf-8') as f:
      f.write('-events\n')

      ev = self.__events
      while ev is not None:
        if isinstance(ev.inner, NullEvent):
          pass
        else:
          tag = ev.inner.get_tag_name()
          ts = format_time_str_from_ms(ev.inner.time_ms)
          fields = ev.inner.fmt()
          f.write('\t'.join((tag, ts, *fields)))
          f.write('\n')

        ev = ev.ll_next
