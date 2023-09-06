from import_data import extract_data

#import data
query = """
SELECT * 
FROM mrt_project_feats 
"""

filename = 'inference_data'

chunk_size= 100000

extract_data().fetchmany(query=query, filename=filename, chunk_size=chunk_size)