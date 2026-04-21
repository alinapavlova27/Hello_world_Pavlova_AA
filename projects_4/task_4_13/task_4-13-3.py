N = int(input("Введите число N: "))

fact = 1
i = 1

while i <= N:
    fact = fact * i
    i = i + 1
print(f"Факториал числа {N} равен {fact}")