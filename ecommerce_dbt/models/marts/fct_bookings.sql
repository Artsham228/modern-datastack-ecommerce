{{ config(materialized='table') }}

with stg_bookings as (
    select * from {{ ref('stg_bookings') }}
),

stg_passengers as (
    select * from {{ ref('stg_passengers') }}
),

stg_flights as (
    select * from {{ ref('stg_flights') }}
)

select
    b.booking_id,
    b.passenger_id,
    b.flight_id,
    b.created_at,
    b.seat_class,
    b.status,
    b.price,
    f.duration_minutes,
    round((b.price / nullif(f.duration_minutes / 60.0, 0))::numeric, 2) as price_per_hour
from stg_bookings b
join stg_passengers p on b.passenger_id = p.passenger_id
join stg_flights f on b.flight_id = f.flight_id