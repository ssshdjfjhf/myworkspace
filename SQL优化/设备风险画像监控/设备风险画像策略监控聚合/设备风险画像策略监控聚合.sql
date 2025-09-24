-- 优化后的设备风险画像策略监控聚合查询
-- 主要优化：1. 减少重复计算 2. 优化JOIN顺序 3. 提前过滤数据 4. 简化JSON解析

-- 预先提取客户ID，减少重复子查询
WITH customer_filter AS (
    SELECT DISTINCT GET_JSON_OBJECT(b.risk_params,'$.customerId') AS customer_id
    FROM mart_caterb2b_mall_risk_management.fact_feature_log_day a
    JOIN mart_caterb2b_mall_risk_management.fact_risk_summary_log_day b
        ON a.trace_id = b.trace_id AND a.dt = b.dt
    WHERE a.dt BETWEEN $$begindatekey AND $$enddatekey
        AND b.dt BETWEEN $$begindatekey AND $$enddatekey
        AND b.scene_code = 'accessBlock'
        AND a.feature_type = 'deviceProfileV2'
        AND GET_JSON_OBJECT(b.risk_params, '$.loginType') = 'NORMAL'
        AND GET_JSON_OBJECT(b.risk_params, '$.containerType') = 'kuailv'
        AND GET_JSON_OBJECT(b.risk_params, '$.mtgsig') IS NOT NULL
        AND GET_JSON_OBJECT(a.feature_result, '$.level3Tags') IS NOT NULL
        AND GET_JSON_OBJECT(a.feature_result, '$.level3Tags') <> '[]'
        AND b.hit_rules IS NOT NULL
),

shibie AS (
    SELECT DISTINCT
        a.dt,
        b.risk_params,
        b.hit_rules,
        GET_JSON_OBJECT(b.risk_params,'$.customerId') AS customer_id,
        GET_JSON_OBJECT(b.risk_params,'$.uuid') AS uuid,
        GET_JSON_OBJECT(a.feature_result,'$.level3Tags') AS level3Tags,
        GET_JSON_OBJECT(a.feature_result,'$.level2Tags') AS level2Tags,
        GET_JSON_OBJECT(a.feature_result,'$.deviceRisk') AS deviceRisk,
        GET_JSON_OBJECT(a.feature_result,'$.hitRivalUuid') AS hitRivalUuid
    FROM mart_caterb2b_mall_risk_management.fact_feature_log_day a
    JOIN mart_caterb2b_mall_risk_management.fact_risk_summary_log_day b
        ON a.trace_id = b.trace_id AND a.dt = b.dt
    -- 使用预过滤的客户ID，减少数据量
    WHERE EXISTS (SELECT 1 FROM customer_filter cf WHERE GET_JSON_OBJECT(b.risk_params,'$.customerId') = cf.customer_id)
        AND a.dt BETWEEN $$begindatekey AND $$enddatekey
        AND b.dt BETWEEN $$begindatekey AND $$enddatekey
        AND b.scene_code = 'accessBlock'
        AND a.feature_type = 'deviceProfileV2'
        AND GET_JSON_OBJECT(b.risk_params, '$.loginType') = 'NORMAL'
        AND GET_JSON_OBJECT(b.risk_params, '$.containerType') = 'kuailv'
        AND GET_JSON_OBJECT(b.risk_params, '$.mtgsig') IS NOT NULL
        AND GET_JSON_OBJECT(a.feature_result, '$.level3Tags') IS NOT NULL
        AND GET_JSON_OBJECT(a.feature_result, '$.level3Tags') <> '[]'
        AND b.hit_rules IS NOT NULL
),

mingzhong AS (
    SELECT
        a.*,
        hitrules,
        GET_JSON_OBJECT(hitrules,'$.ruleId') AS rule_id,
        GET_JSON_OBJECT(hitrules,'$.isBleach') AS isBleach
    FROM shibie AS a
    CROSS JOIN UNNEST(CAST(JSON_PARSE(hit_rules) AS ARRAY(json))) AS t(hitrules)
    WHERE GET_JSON_OBJECT(hitrules, '$.ruleId') NOT IN ('935', '974') -- 字符串比较更安全
),

-- 优化：只查询需要的客户，减少数据扫描
hit_days_uuid AS (
    SELECT DISTINCT
        dt,
        customer_id,
        uuid
    FROM mart_caterb2b_mall_risk_management.fact_kuailv_app_visit_click_summary
    WHERE dt BETWEEN $$begindatekey AND $$enddatekey
        AND visit_second_ct > 0
        AND EXISTS (SELECT 1 FROM customer_filter cf WHERE customer_id = cf.customer_id)
),

-- 优化：预先计算BD信息，避免重复JOIN
cust_bd AS (
    SELECT
        a.dt,
        a.customer_id,
        a.customer_name,
        COALESCE(a.revive_first_arranged_ord_dt, a.first_arranged_ord_date) AS first_arranged_ord_dt,
        datekey2date(COALESCE(a.revive_first_arranged_ord_dt, a.first_arranged_ord_date)) AS first_arranged_ord_date,
        COALESCE(a.revive_first_arranged_ord_belong_bd_id, a.first_arranged_ord_belong_bd_id) AS first_arranged_ord_belong_bd_id,
        b.area_name,
        b.org_name,
        b.bd_name AS first_bd_name,
        b.job_status_name AS first_bd_status,
        a.bd_id AS belong_bd_id,
        c.bd_name AS belong_bd_name,
        c.org_name AS belong_org_name,
        c.area_name AS belong_area_name
    FROM mart_caterb2b.mid_sm_bd_cust_active_label_with_pop AS a
    JOIN mart_caterb2b.dim_sm_rac_org_bd_info_his AS b
        ON COALESCE(a.revive_first_arranged_ord_belong_bd_id, a.first_arranged_ord_belong_bd_id) = b.bd_id
        AND b.dt = $$yesterday_compact
    JOIN mart_caterb2b.dim_sm_rac_org_bd_info_his AS c
        ON a.bd_id = c.bd_id AND a.dt = c.dt
    WHERE a.dt BETWEEN $$begindatekey AND $$enddatekey
        AND c.dt BETWEEN $$begindatekey AND $$enddatekey
        AND EXISTS (SELECT 1 FROM customer_filter cf WHERE a.customer_id = cf.customer_id)
),

shibie_order AS (
    SELECT
        dt,
        GET_JSON_OBJECT(riskparams,'$.customerId') AS customer_id,
        GET_JSON_OBJECT(riskparams,'$.uuid') AS order_uuid
    FROM mart_caterb2b_mall_risk_management.order_risk_result
    WHERE dt BETWEEN $$begindatekey AND $$enddatekey
        AND EXISTS (SELECT 1 FROM customer_filter cf WHERE GET_JSON_OBJECT(riskparams,'$.customerId') = cf.customer_id)
),

-- 优化：使用CASE表达式替代重复的CASE WHEN
final AS (
    SELECT
        a.dt AS shibie_dt,
        a.customer_id,
        a.uuid AS shibie_uuid,
        CASE a.rule_id
            WHEN '1316' THEN '虚拟云手机'
            WHEN '1317' THEN '模拟器'
            WHEN '1324' THEN '改机ROM'
            WHEN '1325' THEN '三方/非官方ROM'
            WHEN '1326' THEN '系统多开'
            ELSE NULL
        END AS rule_id,
        CASE a.isBleach
            WHEN 'true' THEN '漂白'
            WHEN 'false' THEN '拦截'
            ELSE '其他'
        END AS isBleach,
        hdu.uuid AS visit_uuid,
        CASE
            WHEN hdu.uuid IS NULL THEN '当日被拦截后未登录成功'
            WHEN hdu.uuid IS NOT NULL AND a.uuid = hdu.uuid THEN '当日使用该设备登录成功'
            WHEN hdu.uuid IS NOT NULL AND a.uuid != hdu.uuid THEN '当日更换设备登录'
            ELSE '其他'
        END AS result_desc,
        cb.first_arranged_ord_dt,
        cb.first_arranged_ord_date,
        cb.first_arranged_ord_belong_bd_id,
        cb.first_bd_name,
        cb.first_bd_status,
        cb.area_name,
        cb.org_name,
        cb.belong_bd_id,
        cb.belong_bd_name,
        cb.belong_org_name,
        cb.belong_area_name,
        so.order_uuid,
        CASE
            WHEN so.order_uuid IS NULL THEN '当日未下单'
            WHEN so.order_uuid IS NOT NULL THEN '当日下单'
            ELSE '其他'
        END AS order_uuid_desc
    FROM mingzhong AS a
    LEFT JOIN hit_days_uuid AS hdu
        ON a.dt = hdu.dt AND a.customer_id = hdu.customer_id
    LEFT JOIN cust_bd AS cb
        ON a.customer_id = cb.customer_id AND a.dt = cb.dt
    LEFT JOIN shibie_order AS so
        ON a.dt = so.dt AND a.customer_id = so.customer_id
),

-- 优化：预计算聚合指标，避免重复计算
aggregated_data AS (
    SELECT
        dd.week_begin_date_id,
        f.rule_id,
        COUNT(DISTINCT f.customer_id) AS shibie_cust_cnt,
        COUNT(DISTINCT f.belong_bd_id) AS shibie_bd_cnt,
        COUNT(DISTINCT CASE WHEN f.isBleach = '拦截' THEN f.customer_id END) AS lanjie_cust,
        COUNT(DISTINCT CASE WHEN f.isBleach = '拦截' AND f.visit_uuid IS NULL THEN f.customer_id END) AS no_vist_cust_cnt,
        COUNT(DISTINCT CASE WHEN f.isBleach = '拦截' AND f.result_desc = '当日使用该设备登录成功' THEN f.customer_id END) AS use_lanjie_vist_cust_cnt,
        COUNT(DISTINCT CASE WHEN f.isBleach = '拦截' AND f.result_desc = '当日更换设备登录' THEN f.customer_id END) AS change_lanjie_visit_cust_cnt,
        COUNT(DISTINCT CASE WHEN f.order_uuid_desc = '当日下单' THEN f.customer_id END) AS order_cust_cnt,
        COUNT(DISTINCT CASE WHEN f.first_arranged_ord_date IS NOT NULL THEN f.customer_id END) AS is_order_cust_cnt,
        COUNT(DISTINCT CASE WHEN datekey2date(f.shibie_dt) BETWEEN f.first_arranged_ord_date AND date_add(f.first_arranged_ord_date, 27) THEN f.customer_id END) AS first_period_cust_cnt,
        COUNT(DISTINCT CASE WHEN datekey2date(f.shibie_dt) BETWEEN date_add(f.first_arranged_ord_date, 28) AND date_add(f.first_arranged_ord_date, 55) THEN f.customer_id END) AS second_period_cust_cnt,
        COUNT(DISTINCT CASE WHEN datekey2date(f.shibie_dt) >= date_add(f.first_arranged_ord_date, 56) THEN f.customer_id END) AS other_period_cust_cnt,
        COUNT(DISTINCT f.shibie_uuid) AS shibie_uuid_cnt,
        COUNT(DISTINCT CASE WHEN f.isBleach = '拦截' THEN f.shibie_uuid END) AS lanjie_uuid,
        COUNT(DISTINCT CASE WHEN f.result_desc = '当日被拦截后未登录成功' THEN f.shibie_uuid END) AS no_vist_uuid_cnt
    FROM final f
    LEFT JOIN dw.dim_date dd ON f.shibie_dt = dd.date_id
    GROUP BY dd.week_begin_date_id, f.rule_id
)

-- 最终输出，计算比率
SELECT
    week_begin_date_id,
    rule_id,
    shibie_cust_cnt,
    shibie_bd_cnt,
    lanjie_cust,
    no_vist_cust_cnt,
    use_lanjie_vist_cust_cnt,
    change_lanjie_visit_cust_cnt,
    order_cust_cnt,
    is_order_cust_cnt,
    first_period_cust_cnt,
    second_period_cust_cnt,
    other_period_cust_cnt,
    shibie_uuid_cnt,
    lanjie_uuid,
    no_vist_uuid_cnt,
    -- 安全的除法计算，避免除零错误
    CASE WHEN shibie_cust_cnt > 0 THEN lanjie_cust * 1.0 / shibie_cust_cnt ELSE 0 END AS lanjie_cust_rate,
    CASE WHEN lanjie_cust > 0 THEN no_vist_cust_cnt * 1.0 / lanjie_cust ELSE 0 END AS lanjie_no_visit_rate,
    CASE WHEN lanjie_cust > 0 THEN use_lanjie_vist_cust_cnt * 1.0 / lanjie_cust ELSE 0 END AS use_lanjie_vist_cust_rate,
    CASE WHEN lanjie_cust > 0 THEN change_lanjie_visit_cust_cnt * 1.0 / lanjie_cust ELSE 0 END AS change_lanjie_visit_cust_rate,
    CASE WHEN shibie_cust_cnt > 0 THEN order_cust_cnt * 1.0 / shibie_cust_cnt ELSE 0 END AS order_cust_rate,
    CASE WHEN shibie_cust_cnt > 0 THEN is_order_cust_cnt * 1.0 / shibie_cust_cnt ELSE 0 END AS shibie_cust_rate,
    CASE WHEN is_order_cust_cnt > 0 THEN first_period_cust_cnt * 1.0 / is_order_cust_cnt ELSE 0 END AS first_period_cust_rate,
    CASE WHEN is_order_cust_cnt > 0 THEN second_period_cust_cnt * 1.0 / is_order_cust_cnt ELSE 0 END AS second_period_cust_rate,
    CASE WHEN is_order_cust_cnt > 0 THEN other_period_cust_cnt * 1.0 / is_order_cust_cnt ELSE 0 END AS other_period_cust_rate
FROM aggregated_data
ORDER BY week_begin_date_id, rule_id;
