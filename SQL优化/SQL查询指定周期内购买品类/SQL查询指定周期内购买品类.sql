with aggregated_data as (
    SELECT
        customer_id,
        customer_name,
        dt,
        cat1_name,
        cat2_name,
        cat3_name,
        cat4_name,
        sku_name,
        SUM(arranged_amt) as amt,
        SUM(arranged_cnt) as cnt
    FROM mart_caterb2b.mid_deal_order_item_withpop
    WHERE dt BETWEEN 20250718 AND 20250915
    AND customer_id IN ('20628233','24737659','24991578','25176611')
    GROUP BY customer_id, customer_name, dt, cat1_name, cat2_name, cat3_name, cat4_name, sku_name
),
cat1_agg as (
    SELECT customer_id, customer_name, dt, cat1_name,
           SUM(amt) as cat1_amt, SUM(cnt) as cat1_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, cat1_name
),
cat2_agg as (
    SELECT customer_id, customer_name, dt, cat2_name,
           SUM(amt) as cat2_amt, SUM(cnt) as cat2_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, cat2_name
),
cat3_agg as (
    SELECT customer_id, customer_name, dt, cat3_name,
           SUM(amt) as cat3_amt, SUM(cnt) as cat3_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, cat3_name
),
cat4_agg as (
    SELECT customer_id, customer_name, dt, cat4_name,
           SUM(amt) as cat4_amt, SUM(cnt) as cat4_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, cat4_name
),
sku_agg as (
    SELECT customer_id, customer_name, dt, sku_name,
           SUM(amt) as sku_amt, SUM(cnt) as sku_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, sku_name
),
final_result as (
    SELECT
        customer_id,
        customer_name,
        dt,
        MAP_AGG(cat1_name, cat1_amt) as cat1_name_amt_json,
        MAP_AGG(cat1_name, cat1_cnt) as cat1_name_cnt_json
    FROM cat1_agg
    GROUP BY customer_id, customer_name, dt
),
all_agg as (
    select customer_id,customer_name,dt,sum(amt) as amt,sum(cnt) as cnt
    from aggregated_data
    group by customer_id,customer_name,dt
)

SELECT
    f.customer_id,
    f.customer_name,
    f.dt,
    all_agg.amt,
    all_agg.cnt,
    f.cat1_name_amt_json,
    f.cat1_name_cnt_json,
    cat2.cat2_name_amt_json,
    cat2.cat2_name_cnt_json,
    cat3.cat3_name_amt_json,
    cat3.cat3_name_cnt_json,
    cat4.cat4_name_amt_json,
    cat4.cat4_name_cnt_json,
    sku.sku_name_amt_json,
    sku.sku_name_cnt_json
FROM final_result f
JOIN (
    SELECT customer_id, customer_name, dt,
           MAP_AGG(cat2_name, cat2_amt) as cat2_name_amt_json,
           MAP_AGG(cat2_name, cat2_cnt) as cat2_name_cnt_json
    FROM cat2_agg
    GROUP BY customer_id, customer_name, dt
) cat2 ON f.customer_id = cat2.customer_id AND f.dt = cat2.dt
JOIN (
    SELECT customer_id, customer_name, dt,
           MAP_AGG(cat3_name, cat3_amt) as cat3_name_amt_json,
           MAP_AGG(cat3_name, cat3_cnt) as cat3_name_cnt_json
    FROM cat3_agg
    GROUP BY customer_id, customer_name, dt
) cat3 ON f.customer_id = cat3.customer_id AND f.dt = cat3.dt
JOIN (
    SELECT customer_id, customer_name, dt,
           MAP_AGG(cat4_name, cat4_amt) as cat4_name_amt_json,
           MAP_AGG(cat4_name, cat4_cnt) as cat4_name_cnt_json
    FROM cat4_agg
    GROUP BY customer_id, customer_name, dt
) cat4 ON f.customer_id = cat4.customer_id AND f.dt = cat4.dt
JOIN (
    SELECT customer_id, customer_name, dt,
           MAP_AGG(sku_name, sku_amt) as sku_name_amt_json,
           MAP_AGG(sku_name, sku_cnt) as sku_name_cnt_json
    FROM sku_agg
    GROUP BY customer_id, customer_name, dt
) sku ON f.customer_id = sku.customer_id AND f.dt = sku.dt
JOIN all_agg
on f.customer_id = all_agg.customer_id and f.dt = all_agg.dt
ORDER BY f.customer_id, f.customer_name, f.dt





with aggregated_data as (
    SELECT
        customer_id,
        customer_name,
        dt,
        cat1_name,
        cat2_name,
        cat3_name,
        cat4_name,
        sku_name,
        SUM(arranged_amt) as amt,
        SUM(arranged_cnt) as cnt
    FROM mart_caterb2b.mid_deal_order_item_withpop
    WHERE dt BETWEEN '${beginDateKey}' AND '${endDateKey}'
    AND customer_id IN (${customerIdList})
    GROUP BY customer_id, customer_name, dt, cat1_name, cat2_name, cat3_name, cat4_name, sku_name
),
cat1_agg as (
    SELECT customer_id, customer_name, dt, cat1_name,
           SUM(amt) as cat1_amt, SUM(cnt) as cat1_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, cat1_name
),
cat2_agg as (
    SELECT customer_id, customer_name, dt, cat2_name,
           SUM(amt) as cat2_amt, SUM(cnt) as cat2_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, cat2_name
),
cat3_agg as (
    SELECT customer_id, customer_name, dt, cat3_name,
           SUM(amt) as cat3_amt, SUM(cnt) as cat3_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, cat3_name
),
cat4_agg as (
    SELECT customer_id, customer_name, dt, cat4_name,
           SUM(amt) as cat4_amt, SUM(cnt) as cat4_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, cat4_name
),
sku_agg as (
    SELECT customer_id, customer_name, dt, sku_name,
           SUM(amt) as sku_amt, SUM(cnt) as sku_cnt
    FROM aggregated_data
    GROUP BY customer_id, customer_name, dt, sku_name
),
final_result as (
    SELECT
        customer_id,
        customer_name,
        dt,
        MAP_AGG(cat1_name, cat1_amt) as cat1_name_amt_json,
        MAP_AGG(cat1_name, cat1_cnt) as cat1_name_cnt_json
    FROM cat1_agg
    GROUP BY customer_id, customer_name, dt
),
all_agg as (
    select customer_id,customer_name,dt,sum(amt) as amt,sum(cnt) as cnt
    from aggregated_data
    group by customer_id,customer_name,dt
)

SELECT
    f.customer_id,
    f.customer_name,
    f.dt,
    all_agg.amt,
    all_agg.cnt,
    f.cat1_name_amt_json,
    f.cat1_name_cnt_json,
    cat2.cat2_name_amt_json,
    cat2.cat2_name_cnt_json,
    cat3.cat3_name_amt_json,
    cat3.cat3_name_cnt_json,
    cat4.cat4_name_amt_json,
    cat4.cat4_name_cnt_json,
    sku.sku_name_amt_json,
    sku.sku_name_cnt_json
FROM final_result f
JOIN (
    SELECT customer_id, customer_name, dt,
           MAP_AGG(cat2_name, cat2_amt) as cat2_name_amt_json,
           MAP_AGG(cat2_name, cat2_cnt) as cat2_name_cnt_json
    FROM cat2_agg
    GROUP BY customer_id, customer_name, dt
) cat2 ON f.customer_id = cat2.customer_id AND f.dt = cat2.dt
JOIN (
    SELECT customer_id, customer_name, dt,
           MAP_AGG(cat3_name, cat3_amt) as cat3_name_amt_json,
           MAP_AGG(cat3_name, cat3_cnt) as cat3_name_cnt_json
    FROM cat3_agg
    GROUP BY customer_id, customer_name, dt
) cat3 ON f.customer_id = cat3.customer_id AND f.dt = cat3.dt
JOIN (
    SELECT customer_id, customer_name, dt,
           MAP_AGG(cat4_name, cat4_amt) as cat4_name_amt_json,
           MAP_AGG(cat4_name, cat4_cnt) as cat4_name_cnt_json
    FROM cat4_agg
    GROUP BY customer_id, customer_name, dt
) cat4 ON f.customer_id = cat4.customer_id AND f.dt = cat4.dt
JOIN (
    SELECT customer_id, customer_name, dt,
           MAP_AGG(sku_name, sku_amt) as sku_name_amt_json,
           MAP_AGG(sku_name, sku_cnt) as sku_name_cnt_json
    FROM sku_agg
    GROUP BY customer_id, customer_name, dt
) sku ON f.customer_id = sku.customer_id AND f.dt = sku.dt
JOIN all_agg
on f.customer_id = all_agg.customer_id and f.dt = all_agg.dt
ORDER BY f.customer_id, f.customer_name, f.dt