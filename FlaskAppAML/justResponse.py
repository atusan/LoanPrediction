import urllib.request
import os
# If you are using Python 3+, import urllib instead of urllib2

import json 


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
body = str.encode(json.dumps(data))
#example URL: https://ussouthcentral.services.azureml.net/workspaces/91af20abfc58455182eaaa615d581c59/services/da7cdb9359a443f0abdef36d30ce8f1c/execute?api-version=2.0&details=true
url = os.environ.get('URL','https://ussouthcentral.services.azureml.net/workspaces/77f59d794bb7494f9d02fec7fed95b16/services/b5683d42ed4949069a97348505f3fd0f/execute?api-version=2.0&format=swagger')
api_key = os.environ.get('API_KEY','GiwCq7mtZF9BN7l5sXLe5316YLLRQ9tg2W5YmxMLlbKZQ4ZjL8vaLx+kedJCQpOOBLbZ1VDfVlvhE4zl25s9Yw==') # Replace this with the API key for the web service)
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}



req =urllib.request.Request(url, body, headers) 
print(req)
try:
    response =urllib.request.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

    result = response.read()
    print(result) 
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))                 