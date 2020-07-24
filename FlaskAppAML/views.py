"""
Routes and views for the flask application.
"""
import json
import urllib.request
import os

from datetime import datetime
from flask import render_template, request, redirect
from FlaskAppAML import app

from FlaskAppAML.forms import SubmissionForm

BRAIN_ML_KEY=os.environ.get('API_KEY', "GiwCq7mtZF9BN7l5sXLe5316YLLRQ9tg2W5YmxMLlbKZQ4ZjL8vaLx+kedJCQpOOBLbZ1VDfVlvhE4zl25s9Yw==")
BRAIN_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/77f59d794bb7494f9d02fec7fed95b16/services/b5683d42ed4949069a97348505f3fd0f/execute?api-version=2.0&format=swagger")
# Deployment environment variables defined on Azure (pull in with os.environ)

# Construct the HTTP request header
# HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ API_KEY)}

HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ BRAIN_ML_KEY)}

# Our main app page/route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """Renders the home page which is the CNS of the web app currently, nothing pretty."""

    form = SubmissionForm(request.form)

    # Form has been submitted
    if request.method == 'POST' and form.validate():

        # Plug in the data into a dictionary object 
        #  - data from the input form
        #  - text data must be converted to lowercase
        data = {
        "Inputs": {
                "input1":
                [
                    {
                            'Column 0': "0",   
                            'Gender': "Male",   
                            'Married': "No",   
                            'Dependents': "0",   
                            'Education': "Graduate",   
                            'Self_Employed': "No",   
                            'ApplicantIncome': "5849",   
                            'CoapplicantIncome': "0",   
                            'LoanAmount': "1",   
                            'Loan_Amount_Term': "360",   
                            'Credit_History': "1",   
                            'Property_Area': "Urban",   
                            'Loan_Status': "Y",   
                            'which_data': "data_train",   
                    }
                ],
        },
    "GlobalParameters":  {
    }
}

        # Serialize the input data into json string
        body = str.encode(json.dumps(data))

        # Formulate the request
        #req = urllib.request.Request(URL, body, HEADERS)
        req = urllib.request.Request(BRAIN_URL, body, HEADERS)

        # Send this request to the AML service and render the results on page
        try:
            # response = requests.post(URL, headers=HEADERS, data=body)
            response = urllib.request.urlopen(req)
            #print(response)
            respdata = response.read()
            result = json.loads(str(respdata, 'utf-8'))
            result = do_something_pretty(result)
            # result = json.dumps(result, indent=4, sort_keys=True)
            return render_template(
                'result.html',
                title="This is the result from AzureML running our example Student Brain Weight Prediction:",
                result=result)

        # An HTTP error
        except urllib.error.HTTPError as err:
            result="The request failed with status code: " + str(err.code)
            return render_template(
                'result.html',
                title='There was an error',
                result=result)
            #print(err)

    # Just serve up the input form
    return render_template(
        'form.html',
        form=form,
        title='Run App',
        year=datetime.now().year,
        message='Demonstrating a website using Azure ML Api')


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

def do_something_pretty(jsondata):
    """We want to process the AML json result to be more human readable and understandable"""
    import itertools # for flattening a list of tuples below

    # We only want the first array from the array of arrays under "Value" 
    # - it's cluster assignment and distances from all centroid centers from k-means model
    value = jsondata["Results"]["output1"]["value"]["Values"][0]
    #valuelen = len(value)
    print(value)
    # Convert values (a list) to a list of tuples [(cluster#,distance),...]
    # valuetuple = list(zip(range(valuelen-1), value[1:(valuelen)]))
    # Convert the list of tuples to one long list (flatten it)
    # valuelist = list(itertools.chain(*valuetuple))

    # Convert to a tuple for the list
    # data = tuple(list(value[0]) + valuelist)

    # Build a placeholder for the cluster#,distance values
    #repstr = '<tr><td>%d</td><td>%s</td></tr>' * (valuelen-1)
    # print(repstr)
    output='For a brain with the size of : '+value[2]+ "<br/>Our Algorithm would calculate the weight to be: "+ value[4]
    # Build the entire html table for the results data representation
    #tablestr = 'Cluster assignment: %s<br><br><table border="1"><tr><th>Cluster</th><th>Distance From Center</th></tr>'+ repstr + "</table>"
    #return tablestr % data
    return output