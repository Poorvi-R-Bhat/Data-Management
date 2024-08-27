from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class UploadForm(FlaskForm):
    file = FileField('Upload Excel File', validators=[      #to create a file input
        FileRequired(),                                     #ensures the file is uploaded before the form submission
    ])                                                         
    submit = SubmitField('Upload')
