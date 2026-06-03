import psycopg2
import pandas as pd

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5435",
        user="postgres_task",
        password="student",
        database="student"
    )
    print("✓ Подключение установлено")

    query = """
        SELECT
            p.id AS price_id,
            p.product_id,
            pr.name AS product_name,
            pr.category,
            p.price,
            p.created_at
        FROM prices p
        JOIN products pr ON p.product_id = pr.id
        ORDER BY pr.name
    """

    df = pd.read_sql(query, connection)
    connection.close()

    print(df.head(10))
    print(df.info())
    print(f"\nВсего записей: {len(df)}")
    print(f"Уникальных товаров: {df['product_id'].nunique()}")
    print(f"Уникальных категорий: {df['category'].nunique()}")

    print("\n=== Метрики вручную ===")
    metrics = {
        'Среднее (mean)'         : df['price'].mean(),
        'Медиана (median)'       : df['price'].median(),
        'Ст. отклонение (std)'   : df['price'].std(),
        'Минимум (min)'          : df['price'].min(),
        'Максимум (max)'         : df['price'].max(),
    }

    for name, val in metrics.items():
        print(f"  {name:30s}: {val:.2f} руб.")

    q1 = df['price'].quantile(0.25)
    q2 = df['price'].quantile(0.50)
    q3 = df['price'].quantile(0.75)
    iqr = q3 - q1

    print("\n=== Квартильные показатели ===")
    print(f"Q1  (25%): {q1}")
    print(f"Q2  (50%): {q2}")
    print(f"Q3  (75%): {q3}")
    print(f"IQR (Q3-Q1): {iqr}")

    high_price_items = df[df['price'] > q3][['product_name', 'category', 'price']]
    print(f"\n=== Товары с ценой выше Q3 (всего: {len(high_price_items)}) ===")
    if not high_price_items.empty:
        print(high_price_items.to_string(index=False))

    by_category = df.groupby('category')['price'].agg(
        count='count',
        mean='mean',
        median='median',
        std='std'
    ).round(2).sort_values('mean', ascending=False)

    print("\n=== Статистика по категориям ===")
    print(by_category.to_string())

    print(f"\nСамая дорогая категория: {by_category.index[0]}")
    print(f"Самая дешёвая категория: {by_category.index[-1]}")

    price_span = df.groupby('product_name')['price'].agg(
        min_price='min',
        max_price='max'
    )
    price_span['price_span'] = price_span['max_price'] - price_span['min_price']

    top5_span = price_span.sort_values('price_span', ascending=False).head(5)

    print("\n=== Топ-5 товаров с наибольшим разбросом цен ===")
    print(top5_span.to_string())

except Exception as error:
    print(f"Ошибка: {error}")