-- 识别到了多少、实际拦截了多少:分为 客户维度、设备维度
-- 拦截之后的表现:1️⃣切换到正常设备的比例; 2️⃣切到正常设备后下单的比例; 3️⃣BD、城市维度的聚集
WITH shibie AS
(
	SELECT  DISTINCT a.dt
	       ,b.risk_params
	       ,b.hit_rules
	       ,GET_JSON_OBJECT(b.risk_params,'$.customerId') customer_id
	       ,GET_JSON_OBJECT(b.risk_params,'$.uuid') uuid
	-- , GET_JSON_OBJECT(a.feature_result, '$.level3Tags') AS level3Tags
	       ,GET_JSON_OBJECT(a.feature_result,'$.level2Tags') AS level2Tags
	-- , GET_JSON_OBJECT(a.feature_result, '$.deviceRisk') AS deviceRisk
	-- , GET_JSON_OBJECT(a.feature_result, '$.hitRivalUuid') AS hitRivalUuid
	FROM mart_caterb2b_mall_risk_management.fact_feature_log_day a
	JOIN mart_caterb2b_mall_risk_management.fact_risk_summary_log_day b
	ON a.trace_id = b.trace_id AND a.dt = b.dt
	WHERE a.dt BETWEEN $$begindatekey AND $$enddatekey
	AND b.dt BETWEEN $$begindatekey AND $$enddatekey
	AND b.scene_code = 'accessBlock'
	AND a.feature_type = 'deviceProfileV2'
	AND GET_JSON_OBJECT(b.risk_params, '$.loginType') = 'NORMAL'
	AND GET_JSON_OBJECT(b.risk_params, '$.containerType') = 'kuailv'
	AND GET_JSON_OBJECT(b.risk_params, '$.mtgsig') IS NOT null
	AND GET_JSON_OBJECT(a.feature_result, '$.level2Tags') IS NOT null
	AND GET_JSON_OBJECT(a.feature_result, '$.level2Tags') <> '[]' 
), mingzhong AS
(
	SELECT  a.dt
	       ,a.customer_id
	       ,a.uuid
	       ,level2Tag
	FROM shibie AS a
	-- LATERAL VIEW explode(split(REGEXP_REPLACE(level2Tags, '\[|\]', ''), ',')) level2Tag AS level2Tag
 LATERAL VIEW explode(split(regexp_replace(level2Tags, '\[|\]|"', ''), ',')) level2Tag AS level2Tag
	WHERE level2Tag IN ('Device_VMCloudPhone', 'Device_Emulator', 'ROM_Modified', 'ROM_3rd', 'Execution_MultiSys', 'Execution_MultiApp', 'Execution_Root', 'Execution_HiddenRoot', 'Execution_Inject', 'Execution_MalFile', 'Execution_Hook', 'Execution_MockLocation', 'Execution_TamperLocation', 'Network_MITM', 'APP_Root', 'APP_Hook', 'APP_Location', 'APP_AutoClick', 'APP_SysModify', 'Behavior_AbnAppInstall', 'Behavior_AbnBattery', 'Behavior_DevMode', 'Behavior_EnvDebug', 'Behavior_DeviceReset', 'Behavior_Algorithm', 'Behavior_SuspectedAttack', 'Parameter_HID1toN', 'Parameter_LID1toN', 'Parameter_IdNto1', 'Parameter_Illegal', 'Parameter_Mismatch', 'Parameter_Falsify') 
) , hit_days_uuid AS
(
	-- 命中标签客户当日在商城浏览设备, 与命中标签设备不同则认定为更换正常设 备
	SELECT  DISTINCT dt
	       ,customer_id
	       ,uuid
	FROM mart_caterb2b_mall_risk_management.fact_kuailv_app_visit_click_summary
	WHERE dt BETWEEN $$begindatekey AND $$enddatekey
	AND customer_id IN ( SELECT DISTINCT customer_id FROM mingzhong )
	AND visit_second_ct > 0 
) , cust_bd AS
(
	SELECT  distinct a.dt
	       ,a.customer_id
	       ,a.customer_name
	       ,NVL(a.revive_first_arranged_ord_dt,a.first_arranged_ord_date)                   AS first_arranged_ord_dt
	       ,datekey2date(NVL(a.revive_first_arranged_ord_dt,a.first_arranged_ord_date))     AS first_arranged_ord_date
	       ,NVL(a.revive_first_arranged_ord_belong_bd_id,a.first_arranged_ord_belong_bd_id) AS first_arranged_ord_belong_bd_id
	       ,b.area_name                                                                     AS area_name
	       ,b.org_name                                                                      AS org_name
	       ,b.bd_name                                                                       AS first_bd_name
	       ,b.job_status_name                                                               AS first_bd_status
	       ,a.bd_id                                                                         AS belong_bd_id
	       ,c.bd_name                                                                       AS belong_bd_name
	       ,c.org_name                                                                      AS belong_org_name
	       ,c.area_name                                                                     AS belong_area_name
	FROM mart_caterb2b.mid_sm_bd_cust_active_label_with_pop AS a
	JOIN mart_caterb2b.dim_sm_rac_org_bd_info_his AS b
	ON NVL(revive_first_arranged_ord_belong_bd_id, first_arranged_ord_belong_bd_id) = b.bd_id AND b.dt = $$yesterday_compact
	JOIN mart_caterb2b.dim_sm_rac_org_bd_info_his AS c
	ON a.bd_id = c.bd_id AND a.dt = c.dt
	WHERE a.dt BETWEEN $$begindatekey AND $$enddatekey
	AND c.dt BETWEEN $$begindatekey AND $$enddatekey
	AND a.customer_id IN ( SELECT distinct customer_id FROM mingzhong ) 
) , shibie_order AS
(
	SELECT  dt
	       ,GET_JSON_OBJECT(riskparams,'$.customerId') AS customer_id
	       ,GET_JSON_OBJECT(riskparams,'$.uuid')       AS order_uuid
	FROM mart_caterb2b_mall_risk_management.order_risk_result
	WHERE dt BETWEEN $$begindatekey AND $$enddatekey
	AND GET_JSON_OBJECT(riskparams, '$.customerId') IN ( SELECT distinct customer_id FROM mingzhong ) 
), yellow_cust AS
(
	SELECT  customer_id
	       ,new_cust_begin_dt
	       ,is_yellow_line_cust
	       ,is_immediate_loss_process_index_cust
	       ,is_immediate_loss_newa_cust
	       ,is_strategy_triggered
	       ,is_related_cust_newa_or_process_index
	       ,is_immediate_loss_newa_or_process_1arranged
	       ,is_non_visit_app_after_1arranged
	       ,is_loss_newa_cust_cat2_cluster
	FROM mart_caterb2b_mall_risk_management.mid_fake_achievement_features_analyze_da
	WHERE dt = $$yesterday_compact{-1d} 
)
SELECT  a.*
       ,ys.*
FROM
(
	SELECT
	-- a.dt                                                                                                                          AS shibie_dt
 a.customer_id
	       ,CASE WHEN cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-27d} AND $$yesterday_compact THEN "近28天新开"
	             WHEN cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-55d} AND $$yesterday_compact{-28d} THEN "近29~56天新开"  ELSE "其他" END AS new_begin_period
	       ,cb.first_arranged_ord_dt
	       ,cb.first_arranged_ord_date
	       ,cb.first_arranged_ord_belong_bd_id
	       ,cb.first_bd_name
	       ,cb.area_name
	       ,cb.org_name
	       ,collect_set(a.level2Tag)                                                                                                           AS level2Tags
	       ,COUNT(distinct a.uuid)                                                                                                             AS shibie_uuid_cnt
	FROM mingzhong AS a
	LEFT JOIN hit_days_uuid AS hdu
	ON a.dt = hdu.dt AND a.customer_id = hdu.customer_id
	LEFT JOIN cust_bd AS cb
	ON a.customer_id = cb.customer_id AND a.dt = cb.dt
	LEFT JOIN shibie_order AS so
	ON a.dt = so.dt AND a.customer_id = so.customer_id
	WHERE cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-56d} AND $$yesterday_compact -- 走完新客期
	-- AND a.level2Tag = "Behavior_DevMode"
	-- AND cb.belong_bd_name is not null
	-- AND cb.belong_bd_name = "宋道明"
	GROUP BY  a.customer_id
	         ,CASE WHEN cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-27d} AND $$yesterday_compact THEN "近28天新开"
	             WHEN cb.first_arranged_ord_dt BETWEEN $$yesterday_compact{-55d} AND $$yesterday_compact{-28d} THEN "近29~56天新开"  ELSE "其他" END
	         ,cb.first_arranged_ord_dt
	         ,cb.first_arranged_ord_date
	         ,cb.first_arranged_ord_belong_bd_id
	         ,cb.first_bd_name
	         ,cb.area_name
	         ,cb.org_name
	ORDER BY  a.customer_id
) AS a
LEFT JOIN yellow_cust AS ys
ON a.customer_id = ys.customer_id