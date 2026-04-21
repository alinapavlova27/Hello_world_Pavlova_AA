N = int(input("Введите число N: "))

S = 0
i = 1

while i <= N:
    S = S + i
    i = i + 1

print(f"Сумма чисел от 1 до {N} равна {S}")