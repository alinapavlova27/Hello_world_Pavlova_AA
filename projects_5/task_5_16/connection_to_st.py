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

    print("Подключение к базе данных прошло успешно!")

except Exception as error:
    print(f"Ошибка при подключении: {error}")