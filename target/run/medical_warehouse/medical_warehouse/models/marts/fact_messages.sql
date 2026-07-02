
  create view "medical_warehouse"."raw"."fact_messages__dbt_tmp"
    
    
  as (
    WITH base AS (
    SELECT
        message_id,
        channel_name,
        message_date,
        message_text,
        views,
        forwards,
        has_media
    FROM raw.stg_telegram_messages
)
SELECT
    channel_name,
    DATE_TRUNC('day', message_date) AS day,
    COUNT(message_id) AS total_messages,
    SUM(views) AS total_views,
    SUM(forwards) AS total_forwards
FROM base
GROUP BY channel_name, day
  );