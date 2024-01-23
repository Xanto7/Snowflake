-- SQL BI Analyst query examples
-- i
-- Orders per day per shop
SELECT "created_at", "shop_id", COUNT(*) order_count
FROM "orders"
GROUP BY "created_at", "shop_id"

-- Orders per day per print provider
SELECT "created_at", "print_provider_id", COUNT(*) order_count
FROM "orders" o
INNER JOIN "order_items" oi
    ON o."order_id" = oi."order_id"
GROUP BY "created_at", "print_provider_id"

-- Orders per day per sku
SELECT "created_at", "print_provider_sku", COUNT(*) order_count
FROM "orders" o
INNER JOIN "order_items" oi
    ON o."order_id" = oi."order_id"
GROUP BY "created_at", "print_provider_sku"

-- ii Order items per day
SELECT "created_at", SUM("quantity") order_item_count
FROM "orders" o
INNER JOIN "order_items" oi
    ON o."order_id" = oi."order_id"
GROUP BY "created_at"

-- iii Order items on average within one order
SELECT AVG(order_item_count) avg_order_item_count
FROM (
    SELECT SUM("quantity") order_item_count
    FROM "orders" o
    INNER JOIN "order_items" oi
        ON o."order_id" = oi."order_id"
    GROUP BY o."order_id"
)