from flask import Flask, render_template,request
from feature import FeatureExtraction
import numpy as np
# import joblib
# import json 
import requests
app = Flask(__name__)

API_KEY = "ihLwr2uokhHtIZYKQLCE_ADiHWqfvPivU52qNuMMarGA"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/',methods=['GET'])
def hello():
    return render_template('index.html')

@app.route("/", methods=["POST"])
def index(): 
        url = request.form['url']
        obj = FeatureExtraction(url)
        x = obj.getFeaturesList()
        #print(x) 
        #x1 = [obj.getFieldList()]

        payload_scoring={
                "input_data": [
                        {
                                "fields": [
                                        "having_IPhaving_IP_Address",
                                        "URLURL_Length",
                                        "Shortining_Service",
                                        "having_At_Symbol",
                                        "double_slash_redirecting",
                                        "Prefix_Suffix",
                                        "having_Sub_Domain",
                                        "SSLfinal_State",
                                        "Domain_registeration_length",
                                        "Favicon",
                                        "port",
                                        "HTTPS_token",
                                        "Request_URL",
                                        "URL_of_Anchor",
                                        "Links_in_tags",
                                        "SFH",
                                        "Submitting_to_email",
                                        "Abnormal_URL",
                                        "Redirect",
                                        "on_mouseover",
                                        "RightClick",
                                        "popUpWidnow",
                                        "Iframe",
                                        "age_of_domain",
                                        "DNSRecord",
                                        "web_traffic",
                                        "Page_Rank",
                                        "Google_Index",
                                        "Links_pointing_to_page",
                                        "Statistical_report"
                                ],
                                "values": [x]
                        }
                ]
        }
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a3ad9075-6686-4181-8a33-ddf1191ecd8d/predictions?version=2022-11-08', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        predictions = response_scoring.json()
        predict = predictions['predictions'][0]['values'][0][0]
        phishing_prob = predictions['predictions'][0]['values'][0][1][0]
        if(predict==-1):
            url = "https://"+url 
        pred = "It is {0:.2f} % safe to go ".format(100-(predictions['predictions'][0]['values'][0][1][0]*100))
        x=round(predictions['predictions'][0]['values'][0][1][1],2)
        print(x)
        return render_template('index.html',xx =x,url=url )




if __name__ =='__main__':
    app.run(port=5500,debug=True)
