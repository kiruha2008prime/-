from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum

class UserRole(Enum):
    CLIENT = "client"
    COURIER = "courier"
    RESTAURANT = "restaurant"
    ADMIN = "admin"

class OrderStatus(Enum):
    PENDING = "Ожидает подтверждения"
    CONFIRMED = "Подтверждён"
    COOKING = "Готовится"
    DELIVERY = "У курьера"
    COMPLETED = "Доставлен"
    CANCELLED = "Отменён"

@dataclass
class User:
    id: int
    name: str
    phone: str
    email: str
    password: str
    role: UserRole
    address: Optional[str] = None
    bonus: int = 0

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "role": self.role.value,  # Преобразуем Enum в строку
            "address": self.address,
            "bonus": self.bonus
        }

@dataclass
class MenuItem:
    id: int
    restaurant_id: int
    name: str
    description: str
    price: float
    cuisine: str
    rating: float = 0.0

    def to_dict(self):
        return asdict(self)

@dataclass
class Restaurant:
    id: int
    name: str
    address: str
    phone: str
    menu: List[MenuItem] = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "menu": [item.to_dict() for item in (self.menu or [])]
        }

@dataclass
class Courier:
    id: int
    name: str
    phone: str
    current_orders: List[int] = None
    is_active: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "current_orders": self.current_orders or [],
            "is_active": self.is_active
        }

@dataclass
class Order:
    id: int
    client_id: int
    restaurant_id: int
    items: List[Dict]
    status: OrderStatus
    delivery_address: str
    total_price: float
    courier_id: Optional[int] = None
    created_at: str = None

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "restaurant_id": self.restaurant_id,
            "items": self.items,
            "status": self.status.value,  # Преобразуем Enum в строку
            "delivery_address": self.delivery_address,
            "total_price": self.total_price,
            "courier_id": self.courier_id,
            "created_at": self.created_at
        }