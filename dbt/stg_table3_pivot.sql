with tab as (

{# instead of writing down all required columns, dbt_utils.star will add all columns except indicated ones below #}

    {%- set excl_cols = [     
         'column3', 
         'column4'] -%}

    SELECT C.CustomerId,
           {{dbt_utils.star(source('schema','table2'), quote_identifiers=False, except=excl_cols)}},
           EOMONTH(oper_day) Oper_Month                 
    FROM {{ source('schema', 'table2') }} (NOLOCK) T
    LEFT JOIN {{ source('schema', 'Customers') }} (NOLOCK) C on C.id = T.id    
)

{# instead of using tsql's built-in unintuituve pivot method, dbt_utils pivot can be implemented in single line of code #}

    SELECT  T.CustomerId,
            T.Oper_Month,
             {{-dbt_utils.pivot('accType_Name',accType_Name_lst, agg='sum', then_value='column1', suffix='_suffix' )-}}             

      FROM tab T        
      GROUP BY T.CustomerId,
               T.Oper_Month
