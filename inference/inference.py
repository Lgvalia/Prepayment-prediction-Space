import requests
import pandas as pd
import import_data
import datetime

url = 'server/predict_csv' #name of the server has been changed
input_file_path = 'data/inference_data.csv'  #indicate correct file
target = 'target' # exact traget name has been changed

##option1
csv_file = open(input_file_path, 'rb') 
print(f'csv_read at {datetime.datetime.now()}')
##option2
# df_in = pd.read_csv(input_file_path)


##option 1
response = requests.post(url, files={'file':csv_file})
print(f'response_posted {datetime.datetime.now()}')
##option 2
# payload = {'data': df_in.to_dict(orient='records')}
# response = requests.post(url, json=payload)

if response.status_code == 200:
    # Get the prediction as a dictionary
    prediction = response.json()
    df = pd.read_csv(input_file_path)[['CustomerId','AccountId',
                                       target]] 
    print(f'output_df_read {datetime.datetime.now()}')
    for key in prediction:
        df[key] = prediction[key]
    print(f'predictions added to df {datetime.datetime.now()}')
    output_file_path = 'output/inference_data_predicted.csv'    
    df.to_csv(output_file_path)
    print(f'output df saved to csv {datetime.datetime.now()}')
    del df
else:
    # Handle the request error
    print(f"Request failed with status code: {response.status_code}")

csv_file.close()

