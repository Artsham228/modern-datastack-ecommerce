{{ config(materialized='table') }}

select
    passenger_id,
    full_name,
    email
from {{ ref('stg_passengers') }}