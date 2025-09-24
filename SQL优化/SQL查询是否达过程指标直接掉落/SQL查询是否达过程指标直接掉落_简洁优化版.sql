-- 简洁优化版本：最小化改动，提取重复表达式
SELECT
    a.customer_id,
    COALESCE(a.last_revive_datekey, a.fst_arranged_dt) AS new_cust_begin_dt,
    a.is_fst1d_valid_cust_for_business_type_id,
    a.is_fst3d_valid_cust_for_business_type_id,
    a.is_fst7d_valid_cust_for_business_type_id,
    -- 优化后的业务逻辑判断
    CASE
        -- 1天有效客户且当天下单
        WHEN a.is_fst1d_valid_cust_for_business_type_id = 1
             AND date2datekey(to_date(b.last_arranged_ord_time)) = COALESCE(a.last_revive_datekey, a.fst_arranged_dt)
        THEN 1

        -- 3天有效客户（业务类型非5）且0-3天内下单
        WHEN a.is_fst3d_valid_cust_for_business_type_id = 1
             AND b.business_type_id <> 5
             AND DATEDIFF(to_date(b.last_arranged_ord_time), datekey2date(COALESCE(a.last_revive_datekey, a.fst_arranged_dt))) BETWEEN 0 AND 3
        THEN 1

        -- 3天有效客户（业务类型5）且0-4天内下单
        WHEN a.is_fst3d_valid_cust_for_business_type_id = 1
             AND b.business_type_id = 5
             AND DATEDIFF(to_date(b.last_arranged_ord_time), datekey2date(COALESCE(a.last_revive_datekey, a.fst_arranged_dt))) BETWEEN 0 AND 4
        THEN 1

        -- 7天有效客户且0-7天内下单
        WHEN a.is_fst7d_valid_cust_for_business_type_id = 1
             AND DATEDIFF(to_date(b.last_arranged_ord_time), datekey2date(COALESCE(a.last_revive_datekey, a.fst_arranged_dt))) BETWEEN 0 AND 7
        THEN 1

        ELSE 0
    END AS is_drop_imm_process_get
FROM mart_caterb2b.app_data_mart_cust_deal_label_for_risk a
JOIN mart_caterb2b.topic_caterb2b_customer_tag_day_withpop b
    ON a.customer_id = b.customer_id
    AND b.dt = $$yesterday_compact
WHERE a.dt = (
    SELECT MAX(dt)
    FROM mart_caterb2b.app_data_mart_cust_deal_label_for_risk
)
AND COALESCE(a.last_revive_datekey, a.fst_arranged_dt) BETWEEN $$yesterday_compact{-112d} AND $$yesterday_compact;
