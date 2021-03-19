from abc import ABC, abstractmethod
from typing import Type


class IBuilder(ABC):
    @abstractmethod
    def build(self, parsed_data: iter):
        pass
