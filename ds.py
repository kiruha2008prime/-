def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    return total, average


def main():
    print("Программа для вычисления суммы и среднего значения чисел")

    try:
        count = int(input("Введите количество чисел: "))

        numbers = []

        for i in range(count):
            num = float(input(f"Введите число {i+1}: "))
            numbers.append(num)

        total, avg = calculate_average(numbers)

        print("Сумма чисел:", total)
        print("Среднее значение:", avg)

    except ValueError:
        print("Ошибка ввода. Пожалуйста, вводите только числа.")


if __name__ == "__main__":
    main()