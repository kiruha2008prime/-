def get_numbers_from_input(user_input: str):
    numbers = []
    parts = user_input.split()
    for part in parts:
        try:
            num = float(part)
            numbers.append(num)
        except ValueError:
            print(f"Предупреждение: '{part}' не является числом и будет пропущено.")
    return numbers

def calculate_average(num_list):
    if not num_list: 
        return 0
    total = sum(num_list)
    count = len(num_list)
    average = total / count
    return average

if __name__ == "__main__":
    print("Программа для вычисления среднего арифметического")
    user_input = input("Введите числа через пробел: ")

    numbers = get_numbers_from_input(user_input)

    if not numbers:
        print("Не было введено ни одного корректного числа. Среднее арифметическое = 0.")
    else:
        avg = calculate_average(numbers)

        print(f"\nВведенные числа: {numbers}")
        print(f"Количество чисел: {len(numbers)}")
        print(f"Среднее арифметическое: {avg:.2f}")
