#!/usr/bin/env python
# encoding: utf-8

import warnings
warnings.filterwarnings("ignore")

import pickle
import pandas as pd
from flask import Flask,request,jsonify, render_template



app = Flask(__name__)

result = {}

def telecomChurn(body):
    cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 
    'PhoneService', 'MultipleLines','InternetService', 'OnlineSecurity', 
    'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 
    'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 
    'MonthlyCharges', 'TotalCharges']
    
    body = body.split(",")
    body = [float(i) for i in body]

    df = pd.DataFrame([body],columns= cols)

    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    Y_pred_lr = loaded_model.predict(df)
    
    if Y_pred_lr == 1:
        churn = "Yes"
    else:
        churn = "No"

    return churn
   


@app.route('/',methods = ['POST','GET'])
def text_request():
    try:
        if request.method == 'POST':
            body = request.form['content']
            print('hello')

        else:
            body = request.args.get('content')
            print(request.args)
            print(body)
        
        sent = telecomChurn(body)
        result['Telecom_Churn'] = {'summary' : sent}
 
        return jsonify(result)


    except:
        content = "Please input feature values"
        return render_template('index.html', tasks= content)
        
    
if __name__=='__main__':
#     app.run(debug=True)
    app.listen(process.env.PORT || 3000, function(){
    console.log("Express server listening on port %d in %s mode", this.address().port, app.settings.env);
    });
