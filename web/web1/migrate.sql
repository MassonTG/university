-- Додаємо координати до таблиці доставок
ALTER TABLE deliveries
    ADD COLUMN IF NOT EXISTS pickup_lat DOUBLE DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS pickup_lng DOUBLE DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS dropoff_lat DOUBLE DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS dropoff_lng DOUBLE DEFAULT NULL;

-- Додаємо координати до таблиці водіїв
ALTER TABLE drivers
    ADD COLUMN IF NOT EXISTS lat DOUBLE DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS lng DOUBLE DEFAULT NULL;

-- Ставимо стартові позиції водіїв (різні точки Києва)
UPDATE drivers SET lat = 50.4547, lng = 30.5238 WHERE id = 1;
UPDATE drivers SET lat = 50.4320, lng = 30.5050 WHERE id = 2;
UPDATE drivers SET lat = 50.4650, lng = 30.4900 WHERE id = 3;