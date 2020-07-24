from wtforms import Form, StringField, TextAreaField, validators


class SubmissionForm(Form):
    Gender = StringField('Gender', [validators.Length(min=2, max=30)])
    Married = StringField('Married', [validators.Length(min=0, max=30)])
    Dependents = TextAreaField('Dependents', [validators.Length(min=1, max=500)])
    Education = StringField('Education', [validators.Length(min=2, max=30)])
    Self_Employed = StringField('Self_Employed', [validators.Length(min=0, max=30)])
    ApplicantIncome = TextAreaField('ApplicantIncome', [validators.Length(min=1, max=500)])
    CoapplicantIncome = StringField('CoapplicantIncome', [validators.Length(min=2, max=30)])
    Loan_Amount = StringField('LoanAmount', [validators.Length(min=0, max=30)])
    Loan_Amount_Term = TextAreaField('Loan_Amount_Term', [validators.Length(min=1, max=500)])
    Credit_History = StringField('Credit_History', [validators.Length(min=2, max=30)])
    Property_Area = StringField('Property_Area', [validators.Length(min=0, max=30)])
    Loan_Status = TextAreaField('Loan_Status', [validators.Length(min=1, max=500)])
