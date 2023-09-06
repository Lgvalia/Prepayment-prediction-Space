import pandas as pd
from sklearn.metrics import (classification_report,
                             confusion_matrix, 
                             precision_score,
                             recall_score,
                             f1_score,
                             ConfusionMatrixDisplay)

df = pd.read_csv('output/inference_data_predicted.csv')

y_test = df['prepaid_target_y']
y_pred = df['Predicted_label']

report = classification_report(y_test, y_pred)
print(report)

