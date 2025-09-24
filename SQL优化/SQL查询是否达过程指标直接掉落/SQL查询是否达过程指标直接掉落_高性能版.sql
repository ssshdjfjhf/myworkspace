-- 高性能优化版本：优化子查询，提高索引利用率
WITH max_dt_cache AS (
    -- 将MAX(dt)查询结果缓存，避免重复计算
    SELECT MAX(dt) as max_dt
    FROM mart_caterb2b.app_data_mart_cust_deal_label_for_risk
),
base_data AS (
    SELECT
        a.customer_id,
        a.last_revive_datekey,
        a.fst_arranged_dt,
        a.is_fst1d_valid_cust_for_business_type_id,
        a.is_fst3d_valid_cust_for_business_type_id,
        a.is_fst7d_valid_cust_for_business_type_id,
        -- 使用COALESCE替代IF，性能更好
        COALESCE(a.last_revive_datekey, a.fst_arranged_dt) AS new_cust_begin_dt,
        b.last_arranged_ord_time,
        b.business_type_id
    FROM mart_caterb2b.app_data_mart_cust_deal_label_for_risk a
    CROSS JOIN max_dt_cache m
    JOIN mart_caterb2b.topic_caterb2b_customer_tag_day_withpop b
        ON a.customer_id = b.customer_id
        AND b.dt = $$yesterday_compact
    WHERE a.dt = m.max_dt
      AND COALESCE(a.last_revive_datekey, a.fst_arranged_dt)
          BETWEEN $$yesterday_compact{-112d} AND $$yesterday_compact
)
SELECT
    customer_id,
    new_cust_begin_dt,
    is_fst1d_valid_cust_for_business_type_id,
    is_fst3d_valid_cust_for_business_type_id,
    is_fst7d_valid_cust_for_business_type_id,
    -- 优化的业务逻辑：使用更高效的条件判断
    CASE
        WHEN is_fst1d_valid_cust_for_business_type_id = 1
             AND date2datekey(to_date(last_arranged_ord_time)) = new_cust_begin_dt
        THEN 1

        WHEN is_fst3d_valid_cust_for_business_type_id = 1
             AND DATEDIFF(to_date(last_arranged_ord_time), datekey2date(new_cust_begin_dt))
                 BETWEEN 0 AND CASE WHEN business_type_id = 5 THEN 4 ELSE 3 END
        THEN 1

        WHEN is_fst7d_valid_cust_for_business_type_id = 1
             AND DATEDIFF(to_date(last_arranged_ord_time), datekey2date(new_cust_begin_dt))
                 BETWEEN 0 AND 7
        THEN 1

        ELSE 0
    END AS is_drop_imm_process_get
FROM base_data
ORDER BY customer_id;
