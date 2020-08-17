# flask_APP
Flask app using dynamodb to serve as an api

In order to run this Flask app, you need to enter your Azure Machine Learning web application information, Mapbox (leaflet) api key, and S3 bucket information into the my_api_info.py file in Flask_app folder. 

## Using Zappa to upload the Flask app to your AWS

Steps to make the Flask_App work in Zappa

1. Create a user in IAM and get Access Keys (or use your current AccessKeys)
2. If you haven't done it before then install AWSCLI (pip install awscli)
3. Run `aws configure` and set your access keys and the region you would like to use for you DynamoDB
4. ensure the Flask_app is working<br>
5. create virtualenv (you may need to `pip install virtualenv`) <br>
    5a. for windows (and probably Max) `python -m venv \zappenv`<br>
    5b. for Mac `virtualenv zappenv`<br>
6. activate your virtualenv <br>
    6a. for Windows (and probably Mac) `\zappenv\Scripts\activate.bat`<br>
    6b. for Mac `source ./zappenv/bin/activate`<br>
7. install requirements.txt `pip install -r requirements.txt`<br>
    (note) you may need to update pip and remember to include any additional requirements you have added.
    to update pip type `python -m pip install --upgrade pip`
    if you have to upgrade pip you will need to install requirements again.
8. run `zappa init` you are almost always 'ok' if you except the defaults, but you can change them
    (note) you should see a "zappa_settings.json" file appear in your directory.
9. run `zappa deploy dev`
    This is assuming you used the default
10. When this complete you will given a url, that will be running in AWS!

Assuming you have to (or just want to) update your flask application.
1.  Make and test your changes locally
2.  run `zappa update dev`

