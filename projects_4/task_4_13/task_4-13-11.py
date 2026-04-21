n = int(input("Введите количество элементов массива: "))

A = [0] * n

for j in range(n):
    A[j] = float(input(f"Введите элемент A[{j}]: "))

i = 0
sum_value = 0
count = 0

while i < n:
    if i % 2 == 0:                  
        sum_value = sum_value + A[i] 
        count = count + 1             
    i = i + 1

if count > 0:
    avg = sum_value / count
    print(f"Среднее арифметическое элементов с четными индексами: {avg}")
else:
    print("Нет элементов с четными индексами")