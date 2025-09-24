-- 优化版本：减少重复扫描和JOIN操作
WITH aggregated_data AS (
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
-- 一次性计算所有聚合结果，避免重复扫描
final_aggregated AS (
    SELECT
        customer_id,
        customer_name,
        dt,
        -- 总计
        SUM(amt) AS total_amt,
        SUM(cnt) AS total_cnt,
        -- 各级分类聚合
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
    FROM aggregated_data
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
FROM final_aggregated
ORDER BY customer_id, customer_name, dt;
