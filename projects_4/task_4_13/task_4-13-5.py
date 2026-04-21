N = int(input("Введите количество чисел N: "))

x = float(input("Введите число 1: "))

max_value = x

i = 2
while i <= N:
    x = float(input(f"Введите число {i}: "))
    
    if x > max_value:
        max_value = x
    
    i = i + 1

print(f"Максимальное число: {max_value}")