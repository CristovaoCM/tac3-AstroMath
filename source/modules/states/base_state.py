from abc import ABC, abstractmethod


class BaseState(ABC):
    """Interface do Padrão State para todas as telas do jogo."""
    def __init__(self, engine):
        self.engine = engine

    def enter(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass