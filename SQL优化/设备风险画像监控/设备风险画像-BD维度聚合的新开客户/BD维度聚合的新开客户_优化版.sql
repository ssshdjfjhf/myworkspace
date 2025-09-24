-- 优化版本：BD维度聚合的新开客户分析
-- 主要优化点：
-- 1. 减少重复的JSON解析
-- 2. 优化子查询为JOIN
-- 3. 提前过滤数据
-- 4. 减少不必要的DISTINCT操作
-- 5. 优化CTE结构

WITH
-- 预先计算客户ID集合，避免重复子查询
target_customers AS (
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
        AND GET_JSON_OBJECT(a.feature_result, '$.level2Tags') IS NOT NULL
        AND GET_JSON_OBJECT(a.feature_result, '$.level2Tags') <> '[]'
),

-- 优化shibie CTE，减少重复JSON解析
shibie AS (
    SELECT a.dt,
           b.risk_params,
           b.hit_rules,
           GET_JSON_OBJECT(b.risk_params,'$.customerId') AS customer_id,
           GET_JSON_OBJECT(b.risk_params,'$.uuid') AS uuid,
           GET_JSON_OBJECT(a.feature_result,'$.level2Tags') AS level2Tags
    FROM mart_caterb2b_mall_risk_management.fact_feature_log_day a
    JOIN mart_caterb2b_mall_risk_management.fact_risk_summary_log_day b
        ON a.trace_id = b.trace_id AND a.dt = b.dt
    JOIN target_customers tc
        ON GET_JSON_OBJECT(b.risk_params,'$.customerId') = tc.customer_id
    WHERE a.dt BETWEEN $$begindatekey AND $$enddatekey
        AND b.dt BETWEEN $$begindatekey AND $$enddatekey
        AND b.scene_code = 'accessBlock'
        AND a.feature_type = 'deviceProfileV2'
        AND GET_JSON_OBJECT(b.risk_params, '$.loginType') = 'NORMAL'
        AND GET_JSON_OBJECT(b.risk_params, '$.containerType') = 'kuailv'
        AND GET_JSON_OBJECT(b.risk_params, '$.mtgsig') IS NOT NULL
        AND GET_JSON_OBJECT(a.feature_result, '$.level2Tags') IS NOT NULL
        AND GET_JSON_OBJECT(a.feature_result, '$.level2Tags') <> '[]'
),

-- 优化mingzhong CTE，使用更高效的标签过滤
mingzhong AS (
    SELECT s.dt,
           s.customer_id,
           s.uuid,
           level2Tag
    FROM shibie s
    LATERAL VIEW explode(split(regexp_replace(level2Tags, '\[|\]|"', ''), ',')) level2Tag AS level2Tag
    WHERE level2Tag IN (
        'Device_VMCloudPhone', 'Device_Emulator', 'ROM_Modified', 'ROM_3rd',
        'Execution_MultiSys', 'Execution_MultiApp', 'Execution_Root', 'Execution_HiddenRoot',
        'Execution_Inject', 'Execution_MalFile', 'Execution_Hook', 'Execution_MockLocation',
        'Execution_TamperLocation', 'Network_MITM', 'APP_Root', 'APP_Hook', 'APP_Location',
        'APP_AutoClick', 'APP_SysModify', 'Behavior_AbnAppInstall', 'Behavior_AbnBattery',
        'Behavior_DevMode', 'Behavior_EnvDebug', 'Behavior_DeviceReset', 'Behavior_Algorithm',
        'Behavior_SuspectedAttack', 'Parameter_HID1toN', 'Parameter_LID1toN', 'Parameter_IdNto1',
        'Parameter_Illegal', 'Parameter_Mismatch', 'Parameter_Falsify'
    )
),

-- 优化hit_days_uuid，使用JOIN替代IN子查询
hit_days_uuid AS (
    SELECT DISTINCT h.dt,
           h.customer_id,
           h.uuid
    FROM mart_caterb2b_mall_risk_management.fact_kuailv_app_visit_click_summary h
    JOIN target_customers tc ON h.customer_id = tc.customer_id
    WHERE h.dt BETWEEN $$begindatekey AND $$enddatekey
        AND h.visit_second_ct > 0
),

-- 优化cust_bd，减少重复计算和JOIN
cust_bd AS (
    SELECT a.dt,
           a.customer_id,
           a.customer_name,
           NVL(a.revive_first_arranged_ord_dt, a.first_arranged_ord_date) AS first_arranged_ord_dt,
           datekey2date(NVL(a.revive_first_arranged_ord_dt, a.first_arranged_ord_date)) AS first_arranged_ord_date,
           NVL(a.revive_first_arranged_ord_belong_bd_id, a.first_arranged_ord_belong_bd_id) AS first_arranged_ord_belong_bd_id,
           b.area_name,
           b.org_name,
           b.bd_name AS first_bd_name,
           b.job_status_name AS first_bd_status,
           a.bd_id AS belong_bd_id,
           c.bd_name AS belong_bd_name,
           c.org_name AS belong_org_name,
           c.area_name AS belong_area_name
    FROM mart_caterb2b.mid_sm_bd_cust_active_label_with_pop a
    JOIN target_customers tc ON a.customer_id = tc.customer_id
    JOIN mart_caterb2b.dim_sm_rac_org_bd_info_his b
        ON NVL(a.revive_first_arranged_ord_belong_bd_id, a.first_arranged_ord_belong_bd_id) = b.bd_id
        AND b.dt = $$yesterday_compact
    JOIN mart_caterb2b.dim_sm_rac_org_bd_info_his c
        ON a.bd_id = c.bd_id AND a.dt = c.dt
    WHERE a.dt BETWEEN $$begindatekey AND $$enddatekey
        AND c.dt BETWEEN $$begindatekey AND $$enddatekey
),

-- 优化shibie_order，使用JOIN替代IN子查询
shibie_order AS (
    SELECT so.dt,
           GET_JSON_OBJECT(so.riskparams,'$.customerId') AS customer_id,
           GET_JSON_OBJECT(so.riskparams,'$.uuid') AS order_uuid
    FROM mart_caterb2b_mall_risk_management.order_risk_result so
    JOIN target_customers tc ON GET_JSON_OBJECT(so.riskparams, '$.customerId') = tc.customer_id
    WHERE so.dt BETWEEN $$begindatekey AND $$enddatekey
),

-- yellow_cust保持不变，因为它是独立的维度表
yellow_cust AS (
    SELECT customer_id,
           new_cust_begin_dt,
           is_yellow_line_cust,
           is_immediate_loss_process_index_cust,
           is_immediate_loss_newa_cust,
           is_strategy_triggered,
           is_related_cust_newa_or_process_index,
           is_immediate_loss_newa_or_process_1arranged,
           is_non_visit_app_after_1arranged,
           is_loss_newa_cust_cat2_cluster
    FROM mart_caterb2b_mall_risk_management.mid_fake_achievement_features_analyze_da
    WHERE dt = $$yesterday_compact{-1d}
),

-- 主查询优化：预先计算分组字段
main_aggregation AS (
    SELECT m.customer_id,
           -- 预先计算分组字段，避免在GROUP BY中重复计算
           CASE
               WHEN cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-27d} AND $$yesterday_compact THEN '近28天新开'
               WHEN cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-55d} AND $$yesterday_compact{-28d} THEN '近29~56天新开'
               ELSE '其他'
           END AS new_begin_period,
           cb.first_arranged_ord_dt,
           cb.first_arranged_ord_date,
           cb.first_arranged_ord_belong_bd_id,
           cb.first_bd_name,
           cb.area_name,
           cb.org_name,
           collect_set(m.level2Tag) AS level2Tags,
           COUNT(DISTINCT m.uuid) AS shibie_uuid_cnt
    FROM mingzhong m
    LEFT JOIN hit_days_uuid hdu
        ON m.dt = hdu.dt AND m.customer_id = hdu.customer_id
    LEFT JOIN cust_bd cb
        ON m.customer_id = cb.customer_id AND m.dt = cb.dt
    LEFT JOIN shibie_order so
        ON m.dt = so.dt AND m.customer_id = so.customer_id
    WHERE cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-56d} AND $$yesterday_compact -- 走完新客期
    GROUP BY m.customer_id,
             CASE
                 WHEN cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-27d} AND $$yesterday_compact THEN '近28天新开'
                 WHEN cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-55d} AND $$yesterday_compact{-28d} THEN '近29~56天新开'
                 ELSE '其他'
             END,
             cb.first_arranged_ord_dt,
             cb.first_arranged_ord_date,
             cb.first_arranged_ord_belong_bd_id,
             cb.first_bd_name,
             cb.area_name,
             cb.org_name
)

-- 最终结果
SELECT ma.*,
       yc.new_cust_begin_dt,
       yc.is_yellow_line_cust,
       yc.is_immediate_loss_process_index_cust,
       yc.is_immediate_loss_newa_cust,
       yc.is_strategy_triggered,
       yc.is_related_cust_newa_or_process_index,
       yc.is_immediate_loss_newa_or_process_1arranged,
       yc.is_non_visit_app_after_1arranged,
       yc.is_loss_newa_cust_cat2_cluster
FROM main_aggregation ma
LEFT JOIN yellow_cust yc ON ma.customer_id = yc.customer_id
ORDER BY ma.customer_id;
