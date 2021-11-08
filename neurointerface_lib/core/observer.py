from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков.
    """
    @abstractmethod
    def update(self, subject):
        """
        Получить обновление от субъекта.
        """
        pass


class Subject(ABC):

    @abstractmethod
    def attach(self, observer):
        """
        Присоединяет наблюдателя к издателю.
        """
        pass

    @abstractmethod
    def detach(self, observer):
        """
        Отсоединяет наблюдателя от издателя.
        """
        pass

    @abstractmethod
    def notify(self):
        """
        Уведомляет всех наблюдателей о событии.
        """
        pass


class ConcreteSubject(Subject):

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self):
        if self._observers is None:
            raise Exception(
                "Subject without Observers. Attach, please.")
        for observer in self._observers:
            observer.update(self)
