{# tables can be joined using for loop, with its relation alias and not complete names, in few lines of code, hundreds of lines can be generated this way #}

{%- set period_lst = ['1M', '3M']-%}
{%- set temp_dict = {
'tmp_grouped_table1':'table1G',
'tmp_grouped_table2':'table2G',
}-%}

;with target_tab as (
        SELECT RP.Load_month,
               RP.CustomerId,
               SUM(RP.targetcolumn1) targetcolumn1,
               SUM(RP.targetcolumn2) targetcolumn2,
               SUM(RP.targetcolumn3) targetcolumn3,
        FROM {{ ref('targettable') }} (NOLOCK) RP      
        GROUP BY RP.Load_month,
                 RP.CustomerId),


SELECT LS.CustomerId,
       LS.Load_month,
       {{dbt_utils.star(from=ref('table5'), except=['CustomerId','Load_month'], relation_alias='LS', quote_identifiers=False)}},
       {{dbt_utils.star(from=ref('mrt_table3'), except=['CustomerId','Load_month'], relation_alias='LS', quote_identifiers=False)}},

{# in this part columns from joined tables with for loop can be displayed #}

       {%- for tab in temp_dict%}
       {%- for pr in period_lst%}
       {{dbt_utils.star(from=ref(tab+pr),
        quote_identifiers=False, relation_alias=temp_dict[tab]+pr, 
        except=['CustomerId','Load_month'], 
        suffix='_'+temp_dict[tab]+pr)}}, {%endfor-%}{%endfor%}

       CASE WHEN TRP.targetcolumn1 > 0 THEN 1 ELSE 0 END target_y_1,
       CASE WHEN TRP.targetcolumn2 > 0 THEN 1 ELSE 0 END target_y_2,
       CASE WHEN TRP.targetcolumn3 > 0 THEN 1 ELSE 0 END target_y_3
               

FROM {{ ref('table5') }} (NOLOCK) LS
LEFT JOIN {{ ref('mrt_table3') }} (NOLOCK) RPC on RPC.loan_id = LS.accountid and RPC.Oper_Month = LS.Load_month

{# this is join part of for loop #}

{%- for tab in temp_dict%}
{%- for pr in period_lst%}
LEFT JOIN {{ ref(tab+pr) }} {{temp_dict[tab]}}{{pr}} (NOLOCK) on {{temp_dict[tab]}}{{pr}}.CustomerId = LS.CustomerId and {{temp_dict[tab]}}{{pr}}.Load_month = LS.Load_month {%endfor-%}{%endfor%}
LEFT JOIN target_tab TP on TP.CustomerId = LS.CustomerId and EOMONTH(DATEADD(month,1,LS.Load_month)) = TP.Load_month