from flask import render_template, request, redirect, url_for, flash
from werkzeug.exceptions import RequestEntityTooLarge
from app import app, db
from app.forms import UploadForm
from app.models import UserData
from app.utils import validate_excel
from app.models import Upload, UserData
from pytz import timezone
from datetime import datetime
from flask import make_response
from collections import Counter
import json
import matplotlib.pyplot as plt
import io
import base64
from flask import session

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

#function to generate unique identifier for the upload
def generate_upload_id():
    last_upload = Upload.query.order_by(Upload.id.desc()).first() # Query the db for the most recent entry (by ordering results by id in dsc)
    if last_upload:
        last_id = int(last_upload.upload_id.replace('DUP', '')) # is a string like "DUP0001", replace DUP and keeps only 0001 and converts to int 1(helps to increment the id)
        new_id = f"DUP{str(last_id + 1).zfill(4)}"  #inc last id by 1 + add 0 to the last id
    else:
        new_id = "DUP0001"
    return new_id


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm() #UploadForm from the forms.py
    if form.validate_on_submit(): #from Flask WTF
        file = form.file.data     #retrieve the file object from the form.py
        if not file.filename.endswith('.xlsx'): #Attribute created automatically by Filestorage
            # print("xlsx is only allwoed")
            flash('Only .xlsx files are allowed Kindly reupload', 'danger')
            return redirect(url_for('upload_file'))

        is_valid, errors, df = validate_excel(file)
        if not is_valid:
            # Generate error report for download
            error_report = "\n".join(errors)    #join error message and display in new line
            response = make_response(error_report)    #custom http response
            response.headers["Content-Disposition"] = "attachment; filename=validation_errors.txt"    #force download instead of inline
            response.mimetype = "text/plain"
            return response

        # Generate a unique identifier for this upload
        upload_id = generate_upload_id()

        local_timezone = timezone("Asia/Kolkata")
        current_time = datetime.now(local_timezone)

        # Create an Upload record
        new_upload = Upload(upload_id=upload_id, upload_timestamp=current_time)
        db.session.add(new_upload)
        db.session.flush()  # Flush to get the ID for the UserData relationship

        for index, row in df.iterrows():
            data = UserData(
                sno=row['Sno'],
                first_name=row['FirstName'],
                last_name=row['LastName'],
                gender=row['Gender'],
                date_of_birth=row['DateofBirth'],
                upload=new_upload   #FK
            )
            db.session.add(data)

        db.session.commit()
        flash(f'File uploaded and data saved successfully! Upload ID: {upload_id}', "success")
        return redirect(url_for('view_uploaded_data'))

    return render_template('upload.html', form=form)

@app.route('/view_uploaded_data')      #GET
def view_uploaded_data():
    uploads = Upload.query.order_by(Upload.upload_timestamp.desc()).all()  # upload timestamp in dsc
    return render_template('view_uploaded_data.html', uploads=uploads)    

@app.route('/view_data/<upload_id>')
def view_data(upload_id):
    upload = Upload.query.filter_by(upload_id=upload_id).first_or_404()  
    user_data = UserData.query.filter_by(upload_id=upload.id).all()  #all rows where the upload_id  matches the id of the Upload 
    print(user_data) 
    return render_template('view_data.html', user_data=user_data, upload_id=upload_id)


@app.route('/dashboard')
def dashboard():
    # Query the data from the database
    user_data = UserData.query.all()
    uploads = Upload.query.all()

    # Process data to calculate age and group by gender
    current_year = datetime.now().year
    age_gender_data = {
        'labels': [],
        'male': [],
        'female': [],
        'other': []
    }

    for user in user_data:
        age = current_year - user.date_of_birth.year
        age_group = f'{age // 10 * 10}s'  # Group ages into 10s: 20s, 30s, etc.
        if age_group not in age_gender_data['labels']:
            age_gender_data['labels'].append(age_group)   #adds the new age_group if not there
            age_gender_data['male'].append(0)       #initialize 0
            age_gender_data['female'].append(0)    
            age_gender_data['other'].append(0)    

        label_index = age_gender_data['labels'].index(age_group)
        if user.gender == 'M':
            age_gender_data['male'][label_index] += 1
        elif user.gender == 'F':
            age_gender_data['female'][label_index] += 1
        else:
            age_gender_data['other'][label_index] += 1

    # Calculate upload trends
    upload_dates = [upload.upload_timestamp.date() for upload in uploads]   #list of only dates from the timestamp
    upload_trends = {str(date): upload_dates.count(date) for date in set(upload_dates)}

    # Calculate gender ratio
    gender_counts = {
        'male': sum(1 for user in user_data if user.gender == 'M'),
        'female': sum(1 for user in user_data if user.gender == 'F'),
        'other': sum(1 for user in user_data if user.gender not in ['M', 'F'])
    }


    # Convert data to JSON for rendering in JavaScript
    age_gender_data_json = json.dumps(age_gender_data)     #converting dict to to json string (for js)
    upload_trends_json = json.dumps(upload_trends)
    gender_counts_json = json.dumps(gender_counts)

    # Pass the data to the template
    return render_template('dashboard.html', age_gender_data=age_gender_data_json, upload_trends=upload_trends_json, gender_counts=gender_counts_json)

if __name__ == "__main__":
    app.run(debug=True)
