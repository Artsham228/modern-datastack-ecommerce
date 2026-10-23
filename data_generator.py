import random

import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker()
Faker.seed(42)
random.seed(42)

DB_URL = "postgresql://admin:adminpassword@localhost:5432/ecommerce_dwh"


# ---------- ВИМІРИ ----------
def generate_airports(num=20):
    rows = []
    for i in range(1, num + 1):
        rows.append({
            "airport_id": i,
            "airport_name": fake.city() + " International",
            "city": fake.city(),
            "country": fake.country(),
            "iata_code": fake.unique.bothify("???").upper(),
        })
    return pd.DataFrame(rows)


def generate_passengers(num=5000):
    rows = []
    for i in range(1, num + 1):
        rows.append({
            "passenger_id": i,
            "full_name": fake.name(),
            # 10% пропущених email (брудні дані)
            "email": fake.email() if random.random() > 0.1 else None,
            "birth_date": fake.date_of_birth(minimum_age=1, maximum_age=90),
            "registration_date": fake.date_between(start_date="-2y", end_date="today"),
        })
    df = pd.DataFrame(rows)
    # 5% дублікатів (теж навмисно)
    duplicates = df.sample(frac=0.05, random_state=42)
    return pd.concat([df, duplicates], ignore_index=True)


def generate_flights(airports_df, num=1000):
    airport_ids = airports_df["airport_id"].tolist()
    rows = []
    for i in range(1, num + 1):
        origin, destination = random.sample(airport_ids, 2)  # різні аеропорти
        rows.append({
            "flight_id": i,
            "flight_number": fake.bothify("??###").upper(),
            "origin_airport_id": origin,
            "destination_airport_id": destination,
            "departure_time": fake.date_time_between(start_date="-1y", end_date="now"),
            "duration_minutes": random.randint(60, 720),
        })
    return pd.DataFrame(rows)


# ---------- ФАКТИ ----------
def generate_bookings(passengers_df, flights_df, num=5000):
    passenger_ids = passengers_df["passenger_id"].unique().tolist()
    flight_ids = flights_df["flight_id"].tolist()
    prices = {"economy": (50, 300), "business": (300, 900), "first": (900, 2000)}
    rows = []
    for i in range(1, num + 1):
        seat_class = random.choices(["economy", "business", "first"], weights=[80, 15, 5])[0]
        low, high = prices[seat_class]
        rows.append({
            "booking_id": i,
            "passenger_id": random.choice(passenger_ids),
            "flight_id": random.choice(flight_ids),
            "booking_date": fake.date_time_between(start_date="-1y", end_date="now"),
            "seat_class": seat_class,
            "price": round(random.uniform(low, high), 2),
            "status": random.choices(["confirmed", "cancelled", "pending"], weights=[80, 10, 10])[0],
        })
    return pd.DataFrame(rows)


def generate_baggage_claims(bookings_df, num=5000):
    booking_ids = bookings_df["booking_id"].tolist()
    rows = []
    for i in range(1, num + 1):
        rows.append({
            "claim_id": i,
            "booking_id": random.choice(booking_ids),
            "issue_type": random.choice(["lost", "damaged", "delayed"]),
            # 20% порожніх описів
            "description": fake.sentence() if random.random() > 0.2 else None,
            "claim_date": fake.date_time_between(start_date="-1y", end_date="now"),
        })
    return pd.DataFrame(rows)


# ---------- ЗАВАНТАЖЕННЯ В DWH ----------
def load_data_to_dwh(tables):
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()
    for name, df in tables.items():
        print(f"Завантаження {name} ({len(df)} рядків)...")
        # replace = повне перезавантаження
        df.to_sql(name, engine, schema="raw", if_exists="replace", index=False)
    print("Дані успішно завантажені у схему 'raw'!")


if __name__ == "__main__":
    df_airports = generate_airports()
    df_passengers = generate_passengers()
    df_flights = generate_flights(df_airports)
    df_bookings = generate_bookings(df_passengers, df_flights)
    df_claims = generate_baggage_claims(df_bookings)

    load_data_to_dwh({
        "airports": df_airports,
        "passengers": df_passengers,
        "flights": df_flights,
        "bookings": df_bookings,
        "baggage_claims": df_claims,
    })