with source as (
    select * from {{ source('raw_ecommerce', 'passengers') }}
)
select
    passenger_id,
    full_name,
    coalesce(email, 'unknown@airline.com') as email
from source