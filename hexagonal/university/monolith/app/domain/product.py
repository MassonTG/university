from dataclasses import dataclass

@dataclass
class Product:
    id: int | None
    name: str
    price: float

    def validate(self):
        if not self.name or len(self.name) > 100:
            raise ValueError("Invalid name")
        if self.price <= 0:
            raise ValueError("Price must be > 0")
