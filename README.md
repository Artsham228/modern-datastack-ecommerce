# Modern Data Stack: Airline DWH

Навчальний проєкт з дисципліни «Технології сховищ даних» (варіант 22, Авіакомпанія).
Лабораторна робота №1: Extract & Load, побудова «сирого» (Raw) шару сховища.

## Архітектура

Python (Faker + pandas) -> PostgreSQL у Docker (схема `raw`)

## Дані

Генератор створює 5 пов'язаних таблиць:

| Таблиця | Тип | Опис |
|---|---|---|
| airports | вимір | Аеропорти |
| passengers | вимір | Пасажири |
| flights | вимір | Рейси |
| bookings | факт | Бронювання |
| baggage_claims | факт | Заявки щодо багажу |

У даних навмисно залишені «брудні» значення (10% порожніх email, 5% дублікатів пасажирів,
20% порожніх описів у baggage_claims). У Raw-шарі вони зберігаються як є, очищення буде в ЛР №2.

## Як запустити

1. Встановити Python 3.9+, Git, Docker Desktop.
2. Склонувати репозиторій і створити середовище:
```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows (Git Bash)
   pip install -r requirements.txt
```
3. Запустити базу даних:
```bash
   docker compose up -d
```
4. Згенерувати та завантажити дані:
```bash
   python data_generator.py
```

Скрипт ідемпотентний: `if_exists="replace"` дозволяє безпечно запускати його повторно.

## Стек

Python, pandas, Faker, SQLAlchemy, PostgreSQL 15, Docker

## ЛР2: dbt-проєкт `ecommerce_dbt`

Трансформація сирих даних авіакомпанії (схема `raw`) у зіркову схему (схема `analytics`).

- `models/staging/` — очищення (views): `stg_passengers`, `stg_flights`, `stg_airports`, `stg_bookings`
- `models/marts/` — вітрини (tables): `dim_passengers`, `dim_flights`, `fct_bookings`
- `fct_bookings` містить обчислювану метрику `price_per_hour`

Запуск: з папки `ecommerce_dbt` виконати `export DBT_PROFILES_DIR=.`, потім `dbt run`.
`profiles.yml` у репозиторії не зберігається (містить пароль).