SELECT  a.customer_id
       ,if(a.last_revive_datekey IS NOT NULL,a.last_revive_datekey,a.fst_arranged_dt) AS new_cust_begin_dt
       ,a.is_fst1d_valid_cust_for_business_type_id
       ,a.is_fst3d_valid_cust_for_business_type_id
       ,a.is_fst7d_valid_cust_for_business_type_id

       ,if((a.is_fst1d_valid_cust_for_business_type_id = 1 AND date2datekey(to_date(b.last_arranged_ord_time)) = if(a.last_revive_datekey IS NOT NULL,a.last_revive_datekey,a.fst_arranged_dt)) OR (is_fst3d_valid_cust_for_business_type_id = 1 AND business_type_id <> 5 AND DATEDIFF(to_date(b.last_arranged_ord_time),datekey2date(if(a.last_revive_datekey IS NOT NULL,a.last_revive_datekey,a.fst_arranged_dt))) BETWEEN 0 AND 3) OR (is_fst3d_valid_cust_for_business_type_id = 1 AND business_type_id = 5 AND DATEDIFF(to_date(b.last_arranged_ord_time),datekey2date(if(a.last_revive_datekey IS NOT NULL,a.last_revive_datekey,a.fst_arranged_dt))) BETWEEN 0 AND 4) OR (is_fst7d_valid_cust_for_business_type_id = 1 AND DATEDIFF(to_date(b.last_arranged_ord_time),datekey2date(if(a.last_revive_datekey IS NOT NULL,a.last_revive_datekey,a.fst_arranged_dt))) BETWEEN 0 AND 7),1,0) AS is_drop_imm_process_get
FROM mart_caterb2b.app_data_mart_cust_deal_label_for_risk AS a
JOIN mart_caterb2b.topic_caterb2b_customer_tag_day_withpop AS b
ON a.customer_id = b.customer_id AND b.dt = $$yesterday_compact
WHERE a.dt = (
SELECT  MAX(dt)
FROM mart_caterb2b.app_data_mart_cust_deal_label_for_risk) AND if(a.last_revive_datekey IS NOT NULL, a.last_revive_datekey, a.fst_arranged_dt) BETWEEN $$yesterday_compact{-112d} AND $$yesterday_compact