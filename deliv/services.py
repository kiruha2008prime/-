from models import *
from utils import *
from typing import Optional, List
import datetime

# --- Пользователи ---
def register_user(name: str, phone: str, email: str, password: str, role: UserRole, address: str = None) -> User:
    users = read_file("users.txt")
    user_id = get_next_id("users.txt")
    new_user = User(
        id=user_id,
        name=name,
        phone=phone,
        email=email,
        password=password,
        role=role,
        address=address,
    )
    users.append(new_user.to_dict())
    write_file("users.txt", users)

    # Автоматически создаём ресторан для пользователя с ролью RESTAURANT
    if role == UserRole.RESTAURANT:
        register_restaurant(
            name=f"Ресторан {name}",
            address=address or "Адрес не указан",
            phone=phone,
            user_id=user_id
        )

    return new_user

def authenticate_user(email: str, password: str) -> Optional[User]:
    users_data = read_file("users.txt")
    for user_data in users_data:
        user = User(
            id=user_data["id"],
            name=user_data["name"],
            phone=user_data["phone"],
            email=user_data["email"],
            password=user_data["password"],
            role=UserRole(user_data["role"]),
            address=user_data.get("address"),
            bonus=user_data.get("bonus", 0)
        )
        if user.email == email and user.password == password:
            return user
    return None

# --- Меню ---
def add_menu_item(restaurant_id: int, name: str, description: str, price: float, cuisine: str) -> MenuItem:
    # Проверяем, существует ли ресторан с таким ID
    restaurants = read_file("restaurants.txt")
    restaurant_exists = any(r["id"] == restaurant_id for r in restaurants)
    if not restaurant_exists:
        raise ValueError(f"Ресторан с ID {restaurant_id} не существует!")

    menu_items = read_file("menu.txt")
    item_id = get_next_id("menu.txt")
    new_item = MenuItem(
        id=item_id,
        restaurant_id=restaurant_id,
        name=name,
        description=description,
        price=price,
        cuisine=cuisine
    )
    menu_items.append(new_item.to_dict())
    write_file("menu.txt", menu_items)
    return new_item

def get_restaurant_menu(restaurant_id: int) -> List[MenuItem]:
    menu_items_data = read_file("menu.txt")
    menu_items = []
    for item_data in menu_items_data:
        menu_items.append(MenuItem(**item_data))
    return [item for item in menu_items if item.restaurant_id == restaurant_id]

def register_restaurant(name: str, address: str, phone: str, user_id: int) -> Restaurant:
    restaurants = read_file("restaurants.txt")
    restaurant_id = get_next_id("restaurants.txt")
    new_restaurant = Restaurant(
        id=restaurant_id,
        name=name,
        address=address,
        phone=phone,
        menu=[]
    )
    restaurants.append(new_restaurant.to_dict())
    write_file("restaurants.txt", restaurants)
    return new_restaurant

# --- Заказы ---
def create_order(client_id: int, restaurant_id: int, items: List[Dict], delivery_address: str) -> Order:
    orders = read_file("orders.txt")
    order_id = get_next_id("orders.txt")
    total_price = sum(item["price"] * item["quantity"] for item in items)
    new_order = Order(
        id=order_id,
        client_id=client_id,
        restaurant_id=restaurant_id,
        items=items,
        status=OrderStatus.PENDING,
        delivery_address=delivery_address,
        total_price=total_price,
        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    orders.append(new_order.to_dict())
    write_file("orders.txt", orders)
    return new_order

def update_order_status(order_id: int, new_status: OrderStatus, courier_id: Optional[int] = None):
    orders_data = read_file("orders.txt")
    for i, order_data in enumerate(orders_data):
        if order_data["id"] == order_id:
            orders_data[i]["status"] = new_status.value  # Сохраняем строку (например, "Доставлен")
            if courier_id is not None:
                orders_data[i]["courier_id"] = courier_id
    write_file("orders.txt", orders_data)

# --- Курьеры ---
def assign_courier_to_order(order_id: int, courier_id: int):
    couriers_data = read_file("couriers.txt")
    for i, courier_data in enumerate(couriers_data):
        if courier_data["id"] == courier_id:
            if courier_data.get("current_orders") is None:
                courier_data["current_orders"] = []
            courier_data["current_orders"].append(order_id)
    write_file("couriers.txt", couriers_data)
    update_order_status(order_id, OrderStatus.DELIVERY, courier_id)

# --- Отчёты ---
def generate_sales_report(start_date: str, end_date: str) -> List[Dict]:
    orders_data = read_file("orders.txt")
    report = []
    for order_data in orders_data:
        if start_date <= order_data.get("created_at", "") <= end_date:
            report.append({
                "order_id": order_data["id"],
                "client_id": order_data["client_id"],
                "restaurant_id": order_data["restaurant_id"],
                "total_price": order_data["total_price"],
                "status": order_data["status"],
                "date": order_data["created_at"]
            })
    return report