from flask import Flask, render_template, redirect, jsonify, request
from flask_cors import CORS, cross_origin
import aws_controller
import os
import json
import urllib.request
from forms import SubmissionForm
from my_api_info import api_key, azure_ml_url, leaflet_api_key, s3_bucket
import random
import string


NBA_ML_KEY = os.environ.get('API_KEY', api_key)
NBA_ML_URL = os.environ.get('URL', azure_ml_url)


# Deployment environment variables defined on Azure (pull in with os.environ)

# Construct the HTTP request header
HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ NBA_ML_KEY)}

#create am instance of Flask
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["DEBUG"] = True
CORS(app, support_credentials=True)

#route to render dashboard.html
@app.route("/")
@app.route("/dashboard")
def dashboard():
    encoded_data = encode_key(leaflet_api_key)
    print(encoded_data['key'])
    return render_template('dashboard.html', 
                        leaflet_api=leaflet_api_key,
                        key=encoded_data['key'],
                        code=encoded_data['code'],
                        bucket=s3_bucket
                        )

#route to render tableau.html embedded Tableau Public visualization
@app.route("/analysis")
def analysis():
    return render_template('tableau.html', bucket=s3_bucket)

#show the json file of teams data on dynamoDB
@app.route('/teams_json')
def teams_data():
    table = 'teams'
    result = aws_controller.get_all(table)   
    return result

#show the json file of players data on dynamoDB
@app.route('/players_json')
def players_data():
    table = 'players'
    result = aws_controller.get_all(table)
    return result

#predict the NBA salary range using the trained Machine learning mode on Azure Machine Learning studio 
@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
    form = SubmissionForm(request.form)

    # Form has been submitted
    if request.method == 'POST' and form.validate():

        data = {
                    "Inputs": {
                            "input1":
                            [
                                { 
                                        'Salary_class_2-8-greater8': "1",
                                        'FG': form.FG.data.lower(),
                                        'PTS': form.PTS.data.lower(),
                                        'FGA': form.FGA.data.lower(),
                                        'Two_P': form.Two_P.data.lower()
                                }
                            ],
                    },
                    # "GlobalParameters":  {
                    # }
                    "GlobalParameters":  {
                        'The initial learning weights diameter': "0.01",
                     }
                }
        # Serialize the input data into json string
        body = str.encode(json.dumps(data))
    
        # Formulate the request
        req = urllib.request.Request(NBA_ML_URL, body, HEADERS)

        # Send this request to the AML service and render the results on page
        try:
            response = urllib.request.urlopen(req)
            respdata = response.read()
            result = json.loads(str(respdata, 'utf-8'))
            result = get_prediction_data(result)
            return render_template(
                'result.html',
                title="This is the result from AzureML running our prediction:",
                result=result,
                bucket=s3_bucket)

        # An HTTP error
        except urllib.error.HTTPError as err:
            result="The request failed with status code: " + str(err.code)
            return render_template(
                'result.html',
                title='There was an error',
                result=result,
                bucket=s3_bucket)
    
    # Just serve up the input form
    return render_template(
        'form.html',
        form=form,
        title='Run App',
        message='Demonstrating a website using Azure ML Api',
        bucket=s3_bucket)

@app.route("/contact")
def contact():  
    return render_template('contact.html', bucket=s3_bucket)

#encode the api key for security (add a random string into the api key)
def encode_key(key):
    encode_data = {}
    letters = string.ascii_lowercase
    length = random.randint(3,9)
    # print(length)
    random_string = ''.join(random.choice(letters) for i in range(length))
    # print(random_string)
    position = random.randint(1,9)
    # print(position)
    api_key = key[0:position] + random_string + key[position:len(key)]
    # print(api_key)
    code = str(length) + str(position)
    encode_data['key'] = api_key
    encode_data['code'] = code
    # print(encode_data)

    return encode_data


def get_prediction_data(jsondata):
    """to process the AML json result to be more human readable and understandable"""
    import itertools # for flattening a list of tuples below

    #select the result data
    data = jsondata["Results"]["output1"][0]
    
    #select prediction data ("Scored Labels")
    #determine the salary ranges usin result from the Azure Machine Learning model 
    if data['Scored Labels'] == "1":
        output = "$0 - $2,000,000"
    elif data['Scored Labels'] == "2":
        output = "$2,000,000 - $8,000,000"
    else:
        output = " more than $8,000,000"
    
    return output


if __name__ == "__main__":
    app.run(debug=True)


