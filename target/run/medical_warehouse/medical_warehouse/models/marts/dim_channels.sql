
  create view "medical_warehouse"."raw"."dim_channels__dbt_tmp"
    
    
  as (
    SELECT DISTINCT
    channel_name
FROM raw.stg_telegram_messages
  );