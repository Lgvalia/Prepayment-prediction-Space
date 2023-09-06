{# the macro defined in macros folder can be materialized as a table and using variables can be reutilized or multiple tables and timeframes #}

{{
  config(
	materialized = 'table',
	)
}}

{{mcr_disbursement_grouped(ref('table1'), -1)}}