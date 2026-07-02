WITH source AS (
    SELECT
        message_id,
        channel_name,
        date::timestamp AS message_date,
        text AS message_text,
        views,
        forwards,
        has_media
    FROM raw.telegram_messages
)

SELECT * FROM source