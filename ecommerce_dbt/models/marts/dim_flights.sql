{{ config(materialized='table') }}

with flights as (
    select * from {{ ref('stg_flights') }}
),

airports as (
    select * from {{ ref('stg_airports') }}
)

select
    f.flight_id,
    f.flight_number,
    f.departure_time,
    f.duration_minutes,
    f.departure_time + f.duration_minutes * interval '1 minute' as arrival_time,
    o.iata_code as origin_iata,
    o.city as origin_city,
    d.iata_code as destination_iata,
    d.city as destination_city
from flights f
left join airports o on f.origin_airport_id = o.airport_id
left join airports d on f.destination_airport_id = d.airport_id