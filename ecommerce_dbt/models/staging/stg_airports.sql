with source as (
    select * from {{ source('raw_ecommerce', 'airports') }}
)

select
    airport_id,
    airport_name,
    city,
    country,
    upper(iata_code) as iata_code
from source