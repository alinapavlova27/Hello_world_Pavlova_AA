import psycopg2

try:
    # Устанавливаем соединение
    connection = psycopg2.connect(
        host="localhost",          # База в контейнере, но доступна через localhost
        port="5435",               # Порт из секции ports
        user="postgres_task",           # POSTGRES_USER
        password="student",        # POSTGRES_PASSWORD
        database="student"          # POSTGRES_DB
    )
    cursor = connection.cursor()

    # 1. Выполняем запрос
    cursor.execute("SELECT name, category FROM products;")

    # 2. Извлекаем все строки
    products = cursor.fetchall()

    for product in products:
        print(f"Товар: {product[0]} - {product[1]}")

    # Не забываем закрыть курсор
    cursor.close()

except Exception as error:
    print(f"Ошибка при подключении: {error}")