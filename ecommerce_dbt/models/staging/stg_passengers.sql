with source as (
    select * from {{ source('raw_ecommerce', 'passengers') }}
),

deduplicated as (
    select
        *,
        row_number() over (partition by passenger_id order by passenger_id) as rn
    from source
)

select
    passenger_id,
    full_name,
    coalesce(email, 'unknown@airline.com') as email
from deduplicated
where rn = 1