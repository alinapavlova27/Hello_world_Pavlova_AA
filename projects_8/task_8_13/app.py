import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, render_template, jsonify, send_file
from sqlalchemy import create_engine

# --- Создаём Flask-приложение ---
app = Flask(__name__)

# Настройка русских шрифтов для графиков
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# --- ИСПРАВЛЕННЫЙ ENGINE для подключения к БД ---
ENGINE = create_engine(
    "postgresql+psycopg2://postgres_task:student@localhost:5435/student"
)


# =============================================================
#   МАРШРУТЫ
# =============================================================

@app.route("/")
def index():
    """Главная страница"""
    return render_template("index.html")


# --- API для статистики ---
@app.route("/api/stat/<metric>")
def get_stat(metric):
    try:
        # Загружаем данные о ценах из таблицы prices
        df = pd.read_sql("""
            SELECT p.name, p.category, pr.price
            FROM products p
            JOIN prices pr ON p.id = pr.product_id
        """, ENGINE)

        if metric == "mean":
            value = f"{df['price'].mean():.2f}"
            label = "Средняя цена (руб.)"
        elif metric == "median":
            value = f"{df['price'].median():.2f}"
            label = "Медианная цена (руб.)"
        elif metric == "total":
            value = int(df['price'].count())
            label = "Всего ценовых записей"
        elif metric == "min":
            value = f"{df['price'].min():.2f}"
            label = "Минимальная цена (руб.)"
        elif metric == "max":
            value = f"{df['price'].max():.2f}"
            label = "Максимальная цена (руб.)"
        elif metric == "std":
            value = f"{df['price'].std():.2f}"
            label = "Стандартное отклонение (руб.)"
        else:
            return jsonify({"error": "Неизвестная метрика"}), 400

        return jsonify({"label": label, "value": value})

    except Exception as e:
        print(f"ERROR в /api/stat/{metric}: {e}")
        return jsonify({"error": str(e)}), 500


# --- API для графиков ---
@app.route("/api/chart/<kind>")
def get_chart(kind):
    try:
        fig, ax = plt.subplots(figsize=(8, 5))

        # ГРАФИК 1: Гистограмма распределения цен
        if kind == "histogram":
            df = pd.read_sql("""
                SELECT pr.price
                FROM products p
                JOIN prices pr ON p.id = pr.product_id
            """, ENGINE)

            ax.hist(df['price'], bins=15, color='steelblue', edgecolor='white', alpha=0.7)
            ax.set_xlabel('Цена (руб.)')
            ax.set_ylabel('Количество товаров')
            ax.set_title('Распределение цен на товары', fontweight='bold')

            mean_val = df['price'].mean()
            median_val = df['price'].median()
            ax.axvline(mean_val, color='red', linestyle='-', linewidth=2, label=f'Среднее: {mean_val:.0f} руб.')
            ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Медиана: {median_val:.0f} руб.')
            ax.legend()

        # ГРАФИК 2: Столбчатая диаграмма - средние цены по категориям
        elif kind == "categories":
            df = pd.read_sql("""
                SELECT p.category, AVG(pr.price) as avg_price
                FROM products p
                JOIN prices pr ON p.id = pr.product_id
                GROUP BY p.category
                ORDER BY avg_price DESC
            """, ENGINE)

            bars = ax.bar(df['category'], df['avg_price'], color='#4a90d9', edgecolor='white')
            ax.set_xlabel('Категория товара')
            ax.set_ylabel('Средняя цена (руб.)')
            ax.set_title('Средние цены по категориям', fontweight='bold')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            df_all = pd.read_sql("""
                SELECT pr.price
                FROM products p
                JOIN prices pr ON p.id = pr.product_id
            """, ENGINE)
            overall_mean = df_all['price'].mean()
            ax.axhline(overall_mean, color='red', linestyle='--', linewidth=2,
                       label=f'Общее среднее: {overall_mean:.0f} руб.')
            ax.legend()

            for bar, val in zip(bars, df['avg_price']):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                        f'{val:.0f}', ha='center', va='bottom', fontsize=9)

        else:
            plt.close(fig)
            return jsonify({"error": "Неизвестный тип графика"}), 400

        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=120, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)

        return send_file(buf, mimetype="image/png")

    except Exception as e:
        print(f"ERROR в /api/chart/{kind}: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)