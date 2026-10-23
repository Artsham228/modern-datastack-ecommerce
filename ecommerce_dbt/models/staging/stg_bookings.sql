with source as (
    select * from {{ source('raw_ecommerce', 'bookings') }}
)

select
    booking_id,
    passenger_id,
    flight_id,
    cast(booking_date as timestamp) as created_at,
    seat_class,
    status,
    case when price >= 0 then price end as price
from source