-- 优化版本：提取公共表达式，简化逻辑，提高可读性
WITH latest_risk_data AS (
    -- 预先获取最新日期，避免在WHERE中使用子查询
    SELECT
        customer_id,
        last_revive_datekey,
        fst_arranged_dt,
        is_fst1d_valid_cust_for_business_type_id,
        is_fst3d_valid_cust_for_business_type_id,
        is_fst7d_valid_cust_for_business_type_id,
        -- 提取公共表达式：客户开始日期
        COALESCE(last_revive_datekey, fst_arranged_dt) AS new_cust_begin_dt
    FROM mart_caterb2b.app_data_mart_cust_deal_label_for_risk
    WHERE dt = (
        SELECT MAX(dt)
        FROM mart_caterb2b.app_data_mart_cust_deal_label_for_risk
    )
),
filtered_risk_data AS (
    -- 预先过滤日期范围，减少JOIN的数据量
    SELECT *
    FROM latest_risk_data
    WHERE new_cust_begin_dt BETWEEN $$yesterday_compact{-112d} AND $$yesterday_compact
),
enriched_data AS (
    -- JOIN并计算日期差值
    SELECT
        a.*,
        b.last_arranged_ord_time,
        b.business_type_id,
        -- 预计算日期转换和差值
        date2datekey(to_date(b.last_arranged_ord_time)) AS last_ord_datekey,
        DATEDIFF(
            to_date(b.last_arranged_ord_time),
            datekey2date(a.new_cust_begin_dt)
        ) AS days_diff
    FROM filtered_risk_data a
    JOIN mart_caterb2b.topic_caterb2b_customer_tag_day_withpop b
        ON a.customer_id = b.customer_id
        AND b.dt = $$yesterday_compact
)
SELECT
    customer_id,
    new_cust_begin_dt,
    is_fst1d_valid_cust_for_business_type_id,
    is_fst3d_valid_cust_for_business_type_id,
    is_fst7d_valid_cust_for_business_type_id,
    -- 简化的业务逻辑判断
    CASE
        -- 1天有效客户：当天下单
        WHEN is_fst1d_valid_cust_for_business_type_id = 1
             AND last_ord_datekey = new_cust_begin_dt
        THEN 1

        -- 3天有效客户（非业务类型5）：0-3天内下单
        WHEN is_fst3d_valid_cust_for_business_type_id = 1
             AND business_type_id <> 5
             AND days_diff BETWEEN 0 AND 3
        THEN 1

        -- 3天有效客户（业务类型5）：0-4天内下单
        WHEN is_fst3d_valid_cust_for_business_type_id = 1
             AND business_type_id = 5
             AND days_diff BETWEEN 0 AND 4
        THEN 1

        -- 7天有效客户：0-7天内下单
        WHEN is_fst7d_valid_cust_for_business_type_id = 1
             AND days_diff BETWEEN 0 AND 7
        THEN 1

        ELSE 0
    END AS is_drop_imm_process_get
FROM enriched_data
ORDER BY customer_id;
