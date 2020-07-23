from wtforms import Form, StringField, TextAreaField, validators


class SubmissionForm(Form):
    #create string field to let user enter the status data in the html form
    FG = StringField('FG',[validators.Length(min=1, max=3)], default="600")
    PTS = StringField('PTS',[validators.Length(min=1, max=4)],default="1167")
    FGA = StringField('FGA',[validators.Length(min=1, max=4)],default="1158")
    Two_P = StringField('Two_P',[validators.Length(min=1, max=3)],default="592")
    