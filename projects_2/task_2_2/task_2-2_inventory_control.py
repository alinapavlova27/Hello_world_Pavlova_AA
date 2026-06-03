reagent_name = input ("Введите название реактива: ")
reagent_quantity = input ("Введите количество реактива: ")
print (f"Реактив {reagent_name} поступил на склад в количестве {reagent_quantity} шт.")
with open("inventory.txt", "w", encoding="utf-8") as report:
    report.write(f"Реактив {reagent_name} поступил на склад в количестве {reagent_quantity} шт.")