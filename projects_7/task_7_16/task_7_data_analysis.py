import warnings

warnings.filterwarnings('ignore')

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ И ЗАГРУЗКА ДАННЫХ
# ============================================================

conn = psycopg2.connect(
    host="localhost",
    port="5435",
    user="postgres_task",
    password="student",
    database="student"
)

query = """
SELECT 
    p.name AS product_name,
    p.category AS category,
    pr.price AS price
FROM products p
LEFT JOIN prices pr ON p.id = pr.product_id
ORDER BY p.id
"""

df = pd.read_sql(query, conn)
conn.close()

print(f"Загружено {len(df)} записей")
print(df.head())

# ============================================================
# 2. СТАТИСТИЧЕСКИЙ АНАЛИЗ
# ============================================================

all_prices = df['price'].dropna()

print(f"\nОбщая статистика по ценам:")
print(f"  Среднее: {all_prices.mean():.2f} руб.")
print(f"  Медиана: {all_prices.median():.2f} руб.")
print(f"  Мин/Макс: {all_prices.min():.2f} / {all_prices.max():.2f} руб.")
print(f"  Стандартное отклонение: {all_prices.std():.2f} руб.")

q1 = all_prices.quantile(0.25)
q3 = all_prices.quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = all_prices[(all_prices < lower_bound) | (all_prices > upper_bound)]
print(f"\nВыбросы (1.5×IQR): {len(outliers)}")

print(f"\nСтатистика по категориям:")
for cat in df['category'].dropna().unique():
    cat_prices = df[df['category'] == cat]['price'].dropna()
    if len(cat_prices) > 0:
        print(f"  {cat}: средняя={cat_prices.mean():.0f}, медиана={cat_prices.median():.0f}, n={len(cat_prices)}")

# ============================================================
# 3. НАСТРОЙКА СТИЛЯ
# ============================================================

plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'axes.titleweight': 'bold',
})

# ============================================================
# ГРАФИК 1: ГИСТОГРАММА РАСПРЕДЕЛЕНИЯ ЦЕН
# ============================================================

fig1, ax1 = plt.subplots(figsize=(14, 8))

n, bins, patches_list = ax1.hist(all_prices, bins=50, edgecolor='white',
                                 alpha=0.7, color='steelblue')

max_idx = np.argmax(n)
patches_list[max_idx].set_facecolor('coral')
patches_list[max_idx].set_alpha(0.9)

ax1.axvline(all_prices.mean(), color='red', linestyle='-', linewidth=2.5,
            label=f'Среднее = {all_prices.mean():.0f} руб.')
ax1.axvline(all_prices.median(), color='green', linestyle='--', linewidth=2.5,
            label=f'Медиана = {all_prices.median():.0f} руб.')

ax1.set_xlabel('Цена (руб.)', fontsize=12)
ax1.set_ylabel('Количество товаров', fontsize=12)
ax1.set_title('Гистограмма распределения цен на товары', fontsize=16, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

stats_text = f"Всего записей: {len(all_prices)}\nСтанд. отклонение: {all_prices.std():.0f} руб."
ax1.text(0.95, 0.95, stats_text, transform=ax1.transAxes,
         va='top', ha='right', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('task_7_histogram.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================================
# ГРАФИК 2: СТОЛБЧАТАЯ ДИАГРАММА — СРЕДНИЕ ЦЕНЫ ПО КАТЕГОРИЯМ
# ============================================================

fig2, ax2 = plt.subplots(figsize=(12, 7))

category_means = []
category_names = []

for cat in df['category'].dropna().unique():
    cat_prices = df[df['category'] == cat]['price'].dropna()
    if len(cat_prices) > 0:
        category_means.append(cat_prices.mean())
        category_names.append(cat)

# Сортируем по убыванию
sorted_idx = np.argsort(category_means)[::-1]
category_means = [category_means[i] for i in sorted_idx]
category_names = [category_names[i] for i in sorted_idx]

bars = ax2.bar(category_names, category_means, color='steelblue', edgecolor='white', alpha=0.8)

for bar, val in zip(bars, category_means):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 500,
             f'{val:.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax2.set_xlabel('Категория товара', fontsize=12)
ax2.set_ylabel('Средняя цена (руб.)', fontsize=12)
ax2.set_title('Средние цены по категориям товаров', fontsize=16, fontweight='bold')
plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('task_7_mean_prices.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================================
# ГРАФИКИ 3-7: ОТДЕЛЬНЫЕ BOXPLOT ДЛЯ КАЖДОЙ КАТЕГОРИИ
# ============================================================

# Цвета для разных категорий
colors_box = {
    'Электроника': '#4C72B0',
    'Бытовая техника': '#DD8452',
    'Одежда': '#55A868',
    'Книги': '#C44E52',
    'Продукты': '#8172B2'
}

categories_list = ['Электроника', 'Бытовая техника', 'Одежда', 'Книги', 'Продукты']

for cat in categories_list:
    fig, ax = plt.subplots(figsize=(10, 7))

    cat_prices = df[df['category'] == cat]['price'].dropna()

    if len(cat_prices) > 0:
        # Построение boxplot
        bp = ax.boxplot([cat_prices], tick_labels=[cat], patch_artist=True,
                        medianprops=dict(color='white', linewidth=3),
                        flierprops=dict(marker='o', markerfacecolor='red', markersize=10))
        bp['boxes'][0].set_facecolor(colors_box.get(cat, '#888888'))
        bp['boxes'][0].set_alpha(0.7)

        # Вычисляем среднее значение
        mean_val = cat_prices.mean()

        # Добавляем треугольник на график
        ax.scatter(1, mean_val, marker='^', s=120, color='gold',
                   edgecolor='black', zorder=5, label=f'Среднее = {mean_val:.0f} руб.')

        # Добавляем легенду
        ax.legend(loc='upper left', fontsize=10)

        ax.set_ylabel('Цена (руб.)', fontsize=12)
        ax.set_title(f'Boxplot: распределение цен в категории "{cat}"', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        # Статистика на графике (n, медиана)
        stats_text = f"n = {len(cat_prices)}\nМедиана = {cat_prices.median():.0f} руб."
        ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
                va='top', ha='right', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

        plt.tight_layout()
        filename = f'task_7_boxplot_{cat}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()
        print(f"✓ Сохранён: {filename}")
    else:
        print(f"  Нет данных для категории: {cat}")

# ============================================================
# 4. ВЫВОД ТЕКСТА В КОНСОЛЬ
# ============================================================

print("\n" + "=" * 80)
print("ВЫВОДЫ ПО РЕЗУЛЬТАТАМ АНАЛИЗА")
print("=" * 80)

print("""
1. ГИСТОГРАММА

Среднее значение находится выше медианы — это правосторонняя асимметрия. 
Большинство товаров сконцентрировано в левой части графика (дешевые товары), 
но есть небольшое количество очень дорогих товаров, которые тянут среднее 
значение вверх. Красный столбик показывает самый частый диапазон цен. 
Вертикальная ось — количество товаров, горизонтальная — цена в рублях.

Аномалии: На гистограмме отдельные аномалии не выделяются.

2. СТОЛБЧАТАЯ ДИАГРАММА

Электроника и бытовая техника — самые дорогие категории. Одежда, книги и 
продукты находятся в бюджетном сегменте.

Аномалии: Аномалий на данном графике нет.

3. ВЫВОДЫ ПО BOXPLOT

Электроника:
- Медиана (белая линия): Находится на уровне 15500 рублей.
- Межквартильный размах (IQR): Основная часть товаров (50% электроники) 
  сосредоточена между 7000 и 45000 рублей.
- Выбросы: На данном графике выбросы отсутствуют. Все значения, включая 
  максимальные (80000 рублей), находятся в пределах усов.
- Распределение: Среднее значение (26425 рублей) находится выше медианы, 
  что указывает на правостороннюю асимметрию — в категории есть дорогие 
  товары, но они не считаются выбросами по методу 1.5×IQR.

Бытовая техника:
- Медиана (белая линия): Находится на уровне 3900 рублей.
- Межквартильный размах (IQR): Основная часть товаров (50% бытовой техники) 
  сосредоточена между 2500 и 15000 рублей.
- Выбросы: На данном графике значения около 35000-70000 рублей отображаются 
  как выбросы (красные точки вверху). Это происходит потому, что они 
  находятся дальше 1.5 IQR от верхней границы ящика.
- Распределение: Среднее значение (13880 рублей) находится значительно выше 
  медианы — это сильная правосторонняя асимметрия. Основная масса товаров 
  дешевая, но есть небольшое количество очень дорогих товаров-выбросов.

Одежда:
- Медиана (белая линия): Находится на уровне 2100 рублей.
- Межквартильный размах (IQR): Основная часть товаров (50% одежды) 
  сосредоточена между 1500 и 3500 рублей.
- Выбросы: На данном графике выбросы отсутствуют.
- Распределение: Среднее значение (2683 рублей) находится выше медианы — 
  асимметрия не очень сильная.

Книги:
- Медиана (белая линия): Находится на уровне 1100 рублей.
- Межквартильный размах (IQR): Основная часть товаров (50% книг) 
  сосредоточена между 1000 и 1400 рублей.
- Выбросы: На данном графике значения около 2000-4000 рублей отображаются 
  как выбросы (красные точки вверху). Это происходит потому, что они 
  находятся дальше 1.5 IQR от верхней границы ящика.
- Распределение: Среднее значение (1325 рублей) находится немного выше 
  медианы. Основная масса книг имеет низкую цену, но есть небольшое 
  количество дорогих книг-выбросов.

Продукты:
- Медиана (белая линия): Находится на уровне 190 рублей.
- Межквартильный размах (IQR): Основная часть товаров (50% продуктов) 
  сосредоточена между 120 и 420 рублей.
- Выбросы: На данном графике выбросы отсутствуют.
- Распределение: Среднее значение (276 рублей) находится выше медианы, 
  но в целом основная масса данных распределена симметрично вокруг 
  центрального значения. Разброс цен минимальный.
""")

print("\n✅ АНАЛИЗ ЗАВЕРШЕН")
print("✅ Сохраненные файлы:")
print("   - task_7_histogram.png")
print("   - task_7_mean_prices.png")
print("   - task_7_boxplot_Электроника.png")
print("   - task_7_boxplot_Бытовая техника.png")
print("   - task_7_boxplot_Одежда.png")
print("   - task_7_boxplot_Книги.png")
print("   - task_7_boxplot_Продукты.png")