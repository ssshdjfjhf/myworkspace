-- 最优化版本：最简洁高效的实现
WITH base_aggregated AS (
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
)
SELECT
    customer_id,
    customer_name,
    dt,
    -- 总计
    SUM(amt) AS amt,
    SUM(cnt) AS cnt,
    -- 各级分类聚合 - 直接在一个查询中完成所有MAP_AGG操作
    MAP_AGG(cat1_name, amt) AS cat1_name_amt_json,
    MAP_AGG(cat1_name, cnt) AS cat1_name_cnt_json,
    MAP_AGG(cat2_name, amt) AS cat2_name_amt_json,
    MAP_AGG(cat2_name, cnt) AS cat2_name_cnt_json,
    MAP_AGG(cat3_name, amt) AS cat3_name_amt_json,
    MAP_AGG(cat3_name, cnt) AS cat3_name_cnt_json,
    MAP_AGG(cat4_name, amt) AS cat4_name_amt_json,
    MAP_AGG(cat4_name, cnt) AS cat4_name_cnt_json,
    MAP_AGG(sku_name, amt) AS sku_name_amt_json,
    MAP_AGG(sku_name, cnt) AS sku_name_cnt_json
FROM base_aggregated
GROUP BY customer_id, customer_name, dt
ORDER BY customer_id, customer_name, dt;
