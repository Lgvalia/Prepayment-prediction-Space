from fastapi import (FastAPI, 
                     File, 
                     UploadFile, 
                     Response)
from pydantic import BaseModel
import pandas as pd
import pickle

app = FastAPI()


model = pickle.load(open('model_2m_fullprepay.pkl', 'rb'))

@app.post('/predict_csv')
def predict_csv(file: UploadFile = File(...)):
    """post request for predicted from csv file into json"""
    df = pd.read_csv(file.file).drop(columns=['CustomerId','loan_id_snaps','load_date_snaps',
                                              'prepaid_target_y','fullprepaid_target_y','halfprepaid_target_y'], axis=1) 
    file.file.close() 
 
    predicted_labels = model.predict(df).tolist()
    predicted_probas = model.predict_proba(df)[:,1].tolist()

    del df

    return {"Predicted_label": predicted_labels, 'Predicted_proba': predicted_probas}

    




