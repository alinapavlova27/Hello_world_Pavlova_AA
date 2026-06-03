operator_name = input("Введите имя оператора: ")
pressure_value = input("Введите текущее значение давления (Па): ")
with open("sensor_log.txt", "w", encoding="utf-8") as report:
    report.write("оператор\tзначение\n")
    report.write(f"{operator_name}\t{pressure_value}")
print ("Данные успешно сохранены в sensor_log.txt")