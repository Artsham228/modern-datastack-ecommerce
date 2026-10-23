with source as (
    select * from {{ source('raw_ecommerce', 'flights') }}
)

select
    flight_id,
    flight_number,
    origin_airport_id,
    destination_airport_id,
    cast(departure_time as timestamp) as departure_time,
    case when duration_minutes > 0 then duration_minutes end as duration_minutes
from source