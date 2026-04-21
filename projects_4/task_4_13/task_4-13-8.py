n = int(input("Введите количество элементов массива: "))

A = [0] * n

for j in range(n):
    A[j] = float(input(f"Введите элемент A[{j}]: "))

i = 0
count = 0

while i < n:
    if A[i] > 0:
        count = count + 1
    i = i + 1

print(f"Количество положительных чисел в массиве: {count}")