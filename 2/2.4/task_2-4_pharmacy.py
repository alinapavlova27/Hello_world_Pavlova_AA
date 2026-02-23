total_capsules = int(input("Введите общее количество произведенных капсул: "))
package_capacity = int(input("Введите количество капсул в одной упаковке: "))
full_pacages = total_capsules // package_capacity
remaining_capsules = total_capsules % package_capacity
print("---Отчет фасовочного цеха ---")
print(f"Полных упаковок: {full_pacages}")
print(f"Остаток капсул:  {remaining_capsules} ")
