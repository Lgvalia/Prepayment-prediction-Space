{# this is another example of using macro in a different time frame #}

{{
  config(
	materialized = 'table',
	)
}}

{{mcr_disbursement_grouped(ref('table1'), -3)}}