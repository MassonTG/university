from abc import ABC, abstractmethod
from core.domain.order import Order

class OrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> str:
        pass

    @abstractmethod
    def get_by_id(self, order_id: str) -> Order | None:
        pass
