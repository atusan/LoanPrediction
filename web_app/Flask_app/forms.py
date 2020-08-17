from wtforms import Form, StringField, TextAreaField, validators


class SubmissionForm(Form):
    #create string field to let user enter the status data in the html form
    APPINCOME = StringField('APPINCOME',[validators.Length(min=1, max=3)], default="600")
    COAPPINCOME = StringField('COAPPINCOME',[validators.Length(min=1, max=4)],default="1167")
    HISTORY = StringField('HISTORY',[validators.Length(min=1, max=4)],default="1158")
    DEP = StringField('DEP',[validators.Length(min=1, max=3)],default="592")
    EDU = StringField('EDU',[validators.Length(min=1, max=3)], default="600")
    GNR = StringField('GNR',[validators.Length(min=1, max=4)],default="1167")
    LAMOUNT = StringField('LAMOUNT',[validators.Length(min=1, max=4)],default="1158")
    LAMOUNT_T = StringField('LAMOUNT_T',[validators.Length(min=1, max=3)],default="592")
    MRD = StringField('MRD',[validators.Length(min=1, max=3)], default="600")
    PPT_A = StringField('PPT_A',[validators.Length(min=1, max=4)],default="1167")
    SELF_EMP = StringField('SELF_EMP',[validators.Length(min=1, max=4)],default="1158")
    
    