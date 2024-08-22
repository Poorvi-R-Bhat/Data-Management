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

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

def generate_upload_id():
    last_upload = Upload.query.order_by(Upload.id.desc()).first()
    if last_upload:
        last_id = int(last_upload.upload_id.replace('DUP', ''))
        new_id = f"DUP{str(last_id + 1).zfill(4)}"
    else:
        new_id = "DUP0001"
    return new_id


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if not file.filename.endswith('.xlsx'):
            flash('Only .xlsx files are allowed!', 'danger')
            return redirect(url_for('upload_file'))

        is_valid, errors, df = validate_excel(file)
        if not is_valid:
            # Generate error report for download
            error_report = "\n".join(errors)
            response = make_response(error_report)
            response.headers["Content-Disposition"] = "attachment; filename=validation_errors.txt"
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
                upload=new_upload
            )
            db.session.add(data)

        db.session.commit()
        flash(f'File uploaded and data saved successfully! Upload ID: {upload_id}', "success")
        return redirect(url_for('view_uploaded_data'))

    return render_template('upload.html', form=form)

@app.errorhandler(RequestEntityTooLarge)
def handle_file_size_error(e):
    flash('File is too large. Maximum allowed size is 5 MB.', 'danger')
    return redirect(url_for('upload_file'))


@app.route('/view_uploaded_data')
def view_uploaded_data():
    uploads = Upload.query.order_by(Upload.upload_timestamp.desc()).all()
    return render_template('view_uploaded_data.html', uploads=uploads)

@app.route('/view_data/<upload_id>')
def view_data(upload_id):
    upload = Upload.query.filter_by(upload_id=upload_id).first_or_404()
    user_data = UserData.query.filter_by(upload_id=upload.id).all()
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
            age_gender_data['labels'].append(age_group)
            age_gender_data['male'].append(0)
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
    upload_dates = [upload.upload_timestamp.date() for upload in uploads]
    upload_trends = {str(date): upload_dates.count(date) for date in set(upload_dates)}

    # Calculate gender ratio
    gender_counts = {
        'male': sum(1 for user in user_data if user.gender == 'M'),
        'female': sum(1 for user in user_data if user.gender == 'F'),
        'other': sum(1 for user in user_data if user.gender not in ['M', 'F'])
    }


    # Convert data to JSON for rendering in JavaScript
    age_gender_data_json = json.dumps(age_gender_data)
    upload_trends_json = json.dumps(upload_trends)
    gender_counts_json = json.dumps(gender_counts)

    # Pass the data to the template
    return render_template('dashboard.html', age_gender_data=age_gender_data_json, upload_trends=upload_trends_json, gender_counts=gender_counts_json)

if __name__ == "__main__":
    app.run(debug=True)
