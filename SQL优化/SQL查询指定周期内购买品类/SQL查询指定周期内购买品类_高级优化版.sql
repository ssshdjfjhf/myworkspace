-- 高级优化版本：处理MAP_AGG重复键问题并进一步优化
WITH base_data AS (
    SELECT
        customer_id,
        customer_name,
        dt,
        cat1_name,
        cat2_name,
        cat3_name,
        cat4_name,
        sku_name,
        SUM(arranged_amt) AS amt,
        SUM(arranged_cnt) AS cnt
    FROM mart_caterb2b.mid_deal_order_item_withpop
    WHERE dt BETWEEN 20250718 AND 20250915
      AND customer_id IN ('20628233','24737659','24991578','25176611')
    GROUP BY customer_id, customer_name, dt, cat1_name, cat2_name, cat3_name, cat4_name, sku_name
),
-- 预聚合各级分类数据，避免MAP_AGG重复键问题
category_aggregated AS (
    SELECT
        customer_id,
        customer_name,
        dt,
        -- 各级分类预聚合
        cat1_name,
        SUM(amt) AS cat1_amt,
        SUM(cnt) AS cat1_cnt,
        cat2_name,
        SUM(amt) AS cat2_amt,
        SUM(cnt) AS cat2_cnt,
        cat3_name,
        SUM(amt) AS cat3_amt,
        SUM(cnt) AS cat3_cnt,
        cat4_name,
        SUM(amt) AS cat4_amt,
        SUM(cnt) AS cat4_cnt,
        sku_name,
        amt AS sku_amt,
        cnt AS sku_cnt
    FROM base_data
    GROUP BY customer_id, customer_name, dt, cat1_name, cat2_name, cat3_name, cat4_name, sku_name, amt, cnt
),
-- 最终聚合
final_result AS (
    SELECT
        customer_id,
        customer_name,
        dt,
        -- 总计
        SUM(sku_amt) AS total_amt,
        SUM(sku_cnt) AS total_cnt,
        -- 使用COLLECT_SET避免重复，然后转换为MAP
        MAP_FROM_ARRAYS(
            COLLECT_SET(cat1_name),
            COLLECT_SET(cat1_amt)
        ) AS cat1_name_amt_json,
        MAP_FROM_ARRAYS(
            COLLECT_SET(cat1_name),
            COLLECT_SET(cat1_cnt)
        ) AS cat1_name_cnt_json,
        MAP_FROM_ARRAYS(
            COLLECT_SET(cat2_name),
            COLLECT_SET(cat2_amt)
        ) AS cat2_name_amt_json,
        MAP_FROM_ARRAYS(
            COLLECT_SET(cat2_name),
            COLLECT_SET(cat2_cnt)
        ) AS cat2_name_cnt_json,
        MAP_FROM_ARRAYS(
            COLLECT_SET(cat3_name),
            COLLECT_SET(cat3_amt)
        ) AS cat3_name_amt_json,
        MAP_FROM_ARRAYS(
            COLLECT_SET(cat3_name),
            COLLECT_SET(cat3_cnt)
        ) AS cat3_name_cnt_json,
        MAP_FROM_ARRAYS(
            COLLECT_SET(cat4_name),
            COLLECT_SET(cat4_amt)
        ) AS cat4_name_amt_json,
        MAP_FROM_ARRAYS(
            COLLECT_SET(cat4_name),
            COLLECT_SET(cat4_cnt)
        ) AS cat4_name_cnt_json,
        MAP_FROM_ARRAYS(
            COLLECT_SET(sku_name),
            COLLECT_SET(sku_amt)
        ) AS sku_name_amt_json,
        MAP_FROM_ARRAYS(
            COLLECT_SET(sku_name),
            COLLECT_SET(sku_cnt)
        ) AS sku_name_cnt_json
    FROM category_aggregated
    GROUP BY customer_id, customer_name, dt
)
SELECT
    customer_id,
    customer_name,
    dt,
    total_amt AS amt,
    total_cnt AS cnt,
    cat1_name_amt_json,
    cat1_name_cnt_json,
    cat2_name_amt_json,
    cat2_name_cnt_json,
    cat3_name_amt_json,
    cat3_name_cnt_json,
    cat4_name_amt_json,
    cat4_name_cnt_json,
    sku_name_amt_json,
    sku_name_cnt_json
FROM final_result
ORDER BY customer_id, customer_name, dt;
