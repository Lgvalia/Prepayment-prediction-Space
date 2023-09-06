{# instead of writing down aggregate function seprately for each column, lists for its relative aggregations can be written down and then aggregated all elements of the list #}
{# when adding or removing columns from aggregates, elements should be added or removed accordingly in these defined lists, no need to change aggregation script #}

{%- set max_cols = [   
   'column1',
   'column2'
]-%}

{%- set sum_cols = [
   'column3',
   'column4'
] -%}

{%- set first_cols = [
   'column5',
   'column6'
]-%}

{%- set first_col_suffix = '_edited' -%}

{%- set rm_cols = [
    'column7',
    'column8'
]-%}

{%- set excl_cols = max_cols + sum_cols + first_cols + rm_cols -%}
{%- set cols = dbt_utils.get_filtered_columns_in_relation(ref("stg_table3"),excl_cols) -%}

{# for loop as in python can be used to replicate calculations depending on the iterables defined above #}

with tab as (
   SELECT *,
          {%- for col in first_cols%} 
          First_value({{col}}) over (Partition By loan_id, Oper_Month Order By oper_day) as {{col}}{{first_col_suffix}} {% if not loop.last-%}, {%- endif%} 
          {%- endfor %}
   FROM {{ ref('stg_table3') }} (NOLOCK)
),

grouped as (
SELECT {%- for col in cols %} 
        {{col}}, {%-endfor%}
       {%- for col in first_cols %}
        {{col}}{{first_col_suffix}}, {%-endfor%}
       {%- for col in max_cols %}
         ISNULL(MAX({{col}}),0) as {{col}}, {%- endfor %} 
       {%- for col in sum_cols %} 
         SUM({{col}}) as {{col}} {%- if not loop.last%} , {%- endif%} {%- endfor %}      
FROM tab
GROUP BY {%- for col in cols %} 
           {{col}}, 
         {%- endfor%}
         {%- for col in first_cols %} 
           {{col}}{{first_col_suffix}} {%-if not loop.last%} , {%- endif%} 
         {%- endfor%}
)

SELECT *
FROM grouped
