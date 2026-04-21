n = int(input("Введите количество элементов массива: "))

A = [0] * n

for j in range(n):
    A[j] = float(input(f"Введите элемент A[{j}]: "))

i = 0
sum_value = 0

while i < n:
    if i % 2 != 0:        
        sum_value = sum_value + A[i]
    i = i + 1

print(f"Сумма элементов с нечетными индексами: {sum_value}")