from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List


class Observer(ABC):
    """
    Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков.
    """
    @abstractmethod
    def update(self, message: Any):
        """
        Получить обновление от субъекта.
        """
        raise NotImplementedError


class Subject(ABC):

    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._state: Any = ""

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self):
        if len(self._observers) == 0:
            raise Exception(
                "Subject without Observers. Attach, please.")
        for observer in self._observers:
            observer.update(self._state)

    # @abstractmethod
    # def attach(self, observer: Observer):
    #     """
    #     Присоединяет наблюдателя к издателю.
    #     """
    #     raise NotImplementedError

    # @abstractmethod
    # def detach(self, observer: Observer):
    #     """
    #     Отсоединяет наблюдателя от издателя.
    #     """
    #     raise NotImplementedError

    # @abstractmethod
    # def notify(self):
    #     """
    #     Уведомляет всех наблюдателей о событии.
    #     """
    #     raise NotImplementedError


# class ConcreteSubject(Subject):

#     def attach(self, observer: Observer):
#         self._observers.append(observer)

#     def detach(self, observer: Observer):
#         self._observers.remove(observer)

#     def notify(self):
#         if self._observers is None:
#             raise Exception(
#                 "Subject without Observers. Attach, please.")
#         for observer in self._observers:
#             observer.update(self)
