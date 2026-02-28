
import pandas as pd 
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import joblib

class MLCrossCheck:

    def __init__(self):
        self.PredictionProba = None
    
    def LogisticRegPred(self, dataList):

        df_test = pd.DataFrame([dataList], columns=['String 1', 'String 2'])

        
        #Train model
        try:
            df = pd.read_csv('CrossCheckDataTrain.csv', encoding='windows-1252')
        except UnicodeDecodeError:
            print("windows-1252 failed, trying latin1")
            df = pd.read_csv('CrossCheckDataTrain.csv', encoding='latin1')

        #Clean Data 
        df['#1 String'] = df['#1 String'].fillna("")
        df['#2 String'] = df['#2 String'].fillna("")
        X_raw = df['#1 String'] + " " + df['#2 String']
        y_train = df['Quality']


        #Saves model, so it doesn't train every time
        model_file = 'TrainData.joblib'
        vector_file = 'VectorData.joblib'
        if os.path.exists(model_file) and os.path.exists(vector_file):
            model = joblib.load(model_file) 
            vector = joblib.load(vector_file)
        else:
            vector = TfidfVectorizer()
            X_train = vector.fit_transform(X_raw)
            model=LogisticRegression()
            model.fit(X_train, y_train)
            joblib.dump(model, model_file)
            joblib.dump(vector, vector_file)

        
        X_test_raw = df_test['String 1'] + " " + df_test['String 2']
        X_test = vector.transform(X_test_raw)
        predictions = model.predict(X_test)

        self.PredictionProba = model.predict_proba(X_test)
        
        prediction_val = predictions[0]
        return prediction_val
    
    def PredictionScore(self):

        predictions_val_score = self.PredictionProba[0][1]
        predictions_score = round(predictions_val_score, 2) * 100
        
        return predictions_score
