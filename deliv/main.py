from models import *
from services import *
from utils import ensure_data_dir
import getpass

def main_menu():
    print("\n=== Сервис доставки еды (CLI) ===")
    print("1. Регистрация")
    print("2. Авторизация")
    print("3. Выход")
    choice = input("Выберите действие: ")
    return choice

def client_menu(user: User):
    while True:
        print("\n=== Личный кабинет клиента ===")
        print(f"Привет, {user.name}!")
        print("1. Просмотреть меню ресторанов")
        print("2. Оформить заказ")
        print("3. Мои заказы")
        print("4. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            restaurants_data = read_file("restaurants.txt")
            for r_data in restaurants_data:
                restaurant = Restaurant(**r_data)
                print(f"\nРесторан: {restaurant.name} (ID: {restaurant.id})")
                menu = get_restaurant_menu(restaurant.id)
                for item in menu:
                    print(f"  - {item.name}: {item.price} руб. ({item.cuisine})")
        elif choice == "2":
            restaurant_id = int(input("Введите ID ресторана: "))
            menu = get_restaurant_menu(restaurant_id)
            for item in menu:
                print(f"{item.id}. {item.name} - {item.price} руб.")
            items = []
            while True:
                item_id = input("Введите ID блюда (или 'end' для завершения): ")
                if item_id == "end":
                    break
                item_id = int(item_id)
                quantity = int(input("Количество: "))
                item = next((m for m in menu if m.id == item_id), None)
                if item:
                    items.append({"menu_item_id": item_id, "name": item.name, "price": item.price, "quantity": quantity})
            delivery_address = input("Адрес доставки: ")
            order = create_order(user.id, restaurant_id, items, delivery_address)
            print(f"Заказ #{order.id} создан! Статус: {order.status.value}")
        elif choice == "3":
            orders_data = read_file("orders.txt")
            user_orders = []
            for o in orders_data:
                if o["client_id"] == user.id:
                    order = Order(
                        id=o["id"],
                        client_id=o["client_id"],
                        restaurant_id=o["restaurant_id"],
                        items=o["items"],
                        status=OrderStatus(o["status"]),  # Преобразуем строку в OrderStatus
                        delivery_address=o["delivery_address"],
                        total_price=o["total_price"],
                        courier_id=o.get("courier_id"),
                        created_at=o.get("created_at")
                    )
                    user_orders.append(order)
            for order in user_orders:
                print(f"Заказ #{order.id}: {order.status.value}, Сумма: {order.total_price} руб.")
        elif choice == "4":
            break

def courier_menu(user: User):
    while True:
        print("\n=== Личный кабинет курьера ===")
        print(f"Привет, {user.name}!")
        print("1. Доступные заказы")
        print("2. Мои заказы")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            orders_data = read_file("orders.txt")
            available_orders = []
            for o in orders_data:
                if o["status"] == OrderStatus.CONFIRMED.value and o.get("courier_id") is None:
                    order = Order(
                        id=o["id"],
                        client_id=o["client_id"],
                        restaurant_id=o["restaurant_id"],
                        items=o["items"],
                        status=OrderStatus(o["status"]),
                        delivery_address=o["delivery_address"],
                        total_price=o["total_price"],
                        courier_id=o.get("courier_id"),
                        created_at=o.get("created_at")
                    )
                    available_orders.append(order)
            for order in available_orders:
                # Получаем номер телефона клиента
                client_data = next(
                    (u for u in read_file("users.txt") if u["id"] == order.client_id),
                    None
                )
                client_phone = client_data["phone"] if client_data else "Неизвестно"
                print(f"Заказ #{order.id}: {order.delivery_address}, Телефон клиента: {client_phone}, Сумма: {order.total_price} руб.")
            order_id = input("Введите ID заказа для принятия (или 'back' для возврата): ")
            if order_id != "back":
                assign_courier_to_order(int(order_id), user.id)
                print("Заказ принят!")

        elif choice == "2":
            orders_data = read_file("orders.txt")
            my_orders = []
            for o in orders_data:
                if o.get("courier_id") == user.id:
                    order = Order(
                        id=o["id"],
                        client_id=o["client_id"],
                        restaurant_id=o["restaurant_id"],
                        items=o["items"],
                        status=OrderStatus(o["status"]),
                        delivery_address=o["delivery_address"],
                        total_price=o["total_price"],
                        courier_id=o.get("courier_id"),
                        created_at=o.get("created_at")
                    )
                    my_orders.append(order)

            if not my_orders:
                print("У вас нет активных заказов.")
            else:
                for order in my_orders:
                    # Получаем номер телефона клиента
                    client_data = next(
                        (u for u in read_file("users.txt") if u["id"] == order.client_id),
                        None
                    )
                    client_phone = client_data["phone"] if client_data else "Неизвестно"
                    print(f"Заказ #{order.id}: Статус: {order.status.value}, Адрес: {order.delivery_address}, Телефон клиента: {client_phone}, Сумма: {order.total_price} руб.")

                # Добавляем возможность отметить заказ как доставленный
                order_id_input = input("\nВведите ID заказа, чтобы отметить его как доставленный (или 'back' для возврата): ")
                if order_id_input != "back":
                    try:
                        order_id = int(order_id_input)
                        update_order_status(order_id, OrderStatus.COMPLETED)
                        print(f"Заказ #{order_id} отмечен как доставленный!")
                    except ValueError:
                        print("Некорректный ID заказа.")

        elif choice == "3":
            break

def restaurant_menu(user: User):
    while True:
        print("\n=== Личный кабинет ресторана ===")
        print(f"Привет, {user.name}!")
        print("1. Просмотреть заказы")
        print("2. Обновить статус заказа")
        print("3. Добавить блюдо в меню")
        print("4. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            orders_data = read_file("orders.txt")
            restaurant_orders = [Order(**o) for o in orders_data if o["restaurant_id"] == user.id]
            for order in restaurant_orders:
                print(f"Заказ #{order.id}: {order.status.value}, Сумма: {order.total_price} руб.")
        elif choice == "2":
            order_id = int(input("Введите ID заказа: "))
            new_status = input("Новый статус (COOKING/DELIVERY/COMPLETED/CANCELLED): ")
            status_map = {
                "COOKING": OrderStatus.COOKING,
                "DELIVERY": OrderStatus.DELIVERY,
                "COMPLETED": OrderStatus.COMPLETED,
                "CANCELLED": OrderStatus.CANCELLED
            }
            if new_status in status_map:
                update_order_status(order_id, status_map[new_status])
                print("Статус обновлён!")
        elif choice == "3":
            name = input("Название блюда: ")
            description = input("Описание: ")
            price = float(input("Цена: "))
            cuisine = input("Кухня: ")
            try:
                add_menu_item(user.id, name, description, price, cuisine)
                print("Блюдо добавлено!")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif choice == "4":
            break

def admin_menu(user: User):
    while True:
        print("\n=== Админ-панель ===")
        print("1. Сгенерировать отчёт по продажам")
        print("2. Управление пользователями")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            start_date = input("Дата начала (YYYY-MM-DD): ")
            end_date = input("Дата конца (YYYY-MM-DD): ")
            report = generate_sales_report(start_date, end_date)
            print("\nОтчёт по продажам:")
            for entry in report:
                print(f"Заказ #{entry['order_id']}: {entry['total_price']} руб., Статус: {entry['status']}")
        elif choice == "2":
            print("Список пользователей:")
            users_data = read_file("users.txt")
            for user_data in users_data:
                print(f"{user_data['id']}. {user_data['name']} ({user_data['role']})")
        elif choice == "3":
            break

def main():
    ensure_data_dir()
    # Добавим тестовые данные (если их нет)
    if not read_file("users.txt"):
        register_user("Admin", "+79990000000", "admin@delivery.ru", "admin123", UserRole.ADMIN)
        register_user("Client", "+79990000001", "client@delivery.ru", "client123", UserRole.CLIENT, "ул. Ленина, 1")
        register_user("Courier", "+79990000002", "courier@delivery.ru", "courier123", UserRole.COURIER)
        register_user("Restaurant", "+79990000003", "restaurant@delivery.ru", "restaurant123", UserRole.RESTAURANT)
        add_menu_item(4, "Пицца Маргарита", "Классическая пицца", 450.0, "Итальянская")
        add_menu_item(4, "Бургер", "С сыром и беконом", 350.0, "Американская")

    while True:
        choice = main_menu()
        if choice == "1":
            print("\nРегистрация")
            name = input("Имя: ")
            phone = input("Телефон: ")
            email = input("Email: ")
            password = getpass.getpass("Пароль: ")
            role = input("Роль (client/courier/restaurant/admin): ")
            role_map = {
                "client": UserRole.CLIENT,
                "courier": UserRole.COURIER,
                "restaurant": UserRole.RESTAURANT,
                "admin": UserRole.ADMIN
            }
            if role in role_map:
                address = input("Адрес (для клиента): ") if role == "client" else None
                register_user(name, phone, email, password, role_map[role], address)
                print("Регистрация успешна!")
            else:
                print("Некорректная роль!")
        elif choice == "2":
            email = input("Email: ")
            password = getpass.getpass("Пароль: ")
            user = authenticate_user(email, password)
            if user:
                if user.role == UserRole.CLIENT:
                    client_menu(user)
                elif user.role == UserRole.COURIER:
                    courier_menu(user)
                elif user.role == UserRole.RESTAURANT:
                    restaurant_menu(user)
                elif user.role == UserRole.ADMIN:
                    admin_menu(user)
            else:
                print("Неверный email или пароль!")
        elif choice == "3":
            print("До свидания!")
            break

if __name__ == "__main__":
    main()