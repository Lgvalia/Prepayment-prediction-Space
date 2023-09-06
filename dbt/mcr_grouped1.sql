{# This macro uses variable as main_table and last_n_months, meaning it can be used with multiple table dynimacally #}

{% macro mcr_grouped(main_table, last_n_months) %}

with tab as (
            SELECT Column1
            	  ,Column2            	  
            	  ,UserId
				  ,Timestamp            	  	              
            FROM {{ source('schema', 'table') }} (NOLOCK) LD            
            )
    SELECT CA.CustomerId
		  ,CA.[Load_month]
		  ,MAX(LD.Timestamp) Max_Disburse_Date
		  ,MIN(LD.Timestamp) Min_Disburse_Date
		  ,SUM(LD.Column1) Column1
		  ,COUNT(LD.Column2) Column2
	FROM tab LD
	JOIN {{main_table}} (NOLOCK) CA on LD.UserId = CA.CustomerId and LD.TimeStamp <= CA.[Load_month]
	WHERE LD.TimeStamp >= DATEADD(month, {{last_n_months}}, CA.Load_month)
	GROUP BY CA.CustomerId
		    ,CA.[Load_month] 
  
{% endmacro %}