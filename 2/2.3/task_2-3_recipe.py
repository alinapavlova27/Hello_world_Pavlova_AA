medium_name = input("Введите название питательной среды: ")
agar_concentration = input("Введите концентрацию агара (%): ")
sterilization_temp = input("Введите температуру стерилизации (°C): ")
with open("recipe.txt", "w", encoding="utf-8") as report:
    report.write(f"Введите название питательной среды: {medium_name}\n")
    report.write(f"Введите концентрацию агара (%): {agar_concentration}\n")
    report.write(f"Введите температуру стерилизации (°C): {sterilization_temp}\n")
print("Файл 'recipe.txt' успешно сформирован!")
