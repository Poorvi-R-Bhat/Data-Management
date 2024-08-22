## Data Management Web Application

## 🚀 Introduction
The Data Management System is a  web application that allows users to upload Excel files containing specific data. The application validates the file structure and content, provides feedback on any validation errors, and saves the valid data into a database. Additionally, users can view the uploaded data and visualize it through a dashboard.

## ✨ Key Features

- Upload `.xlsx` files via a user-friendly web interface.
- Validate the uploaded Excel file for required columns, data types, and formats.
- Report validation errors, including the ability to download a detailed error report.
- Insert valid data into a database.
- View uploaded data and manage records.
- Dashboard with visualizations showing the number of users based on age and gender.

## 🛠 Setup and Installation

### Prerequisites:
- Python 3.x
- Flask
- SQLAlchemy
- Pandas
- Matplotlib
- Chart.js (for dashboard visualizations)
- SQLite (or any other SQL database)
  
```bash
   git clone https://github.com/Poorvi-R-Bhat/Data-Management.git
```

### Usage Instructions
Uploading Files:
Navigate to the Upload page.
Upload a .xlsx file with the required structure.
If validation errors occur, download the error report to correct the file.
Upon successful validation, the data is stored in the database.

Viewing Uploaded Data:
Access the View Uploaded Data page to see records of past uploads. You can view the details of each uploaded dataset.

Dashboard:
The dashboard provides a graphical representation of user data based on gender and age groups.

### 1. Home Page:

![image](https://github.com/user-attachments/assets/38573671-6fbc-4d37-ae4b-cc2992fc48b7)

### 2. File upload interface

- The application provides a web interface that allows users to upload an Excel file.
- Only files with the `.xlsx` extension are accepted.
  ![image](https://github.com/user-attachments/assets/36a08c59-447f-4be2-b756-4a20de971f0c)

### 3. File Structure Validation
- The uploaded Excel file must contain exactly five columns:
  1. `Sno`
  2. `FirstName`
  3. `LastName`
  4. `Gender`
  5. `DateofBirth`
- The application validates the presence and exact names of these columns. Any deviation results in a validation error.


### 4. Data Insertion:
- After successful validation, the data is inserted into a database table that mirrors the structure of the Excel file.
- Each upload is tracked with a unique identifier (e.g., `DUP0001`, `DUP0002`).

  ![image](https://github.com/user-attachments/assets/1122f962-ff13-4401-b8fe-3a67e1fbec9e)


### 5. Viewing the uploaded data
![image](https://github.com/user-attachments/assets/1bf4af7c-6b38-4c5c-9c46-76e9cb23e0d0)


### 6. Viewing the dashboard
- Age and Gender distribution
![image](https://github.com/user-attachments/assets/9fb9e561-4205-436f-9a70-21613c36ef9c)

- Upload trends
![image](https://github.com/user-attachments/assets/750700b4-412d-427d-b48c-e5304f22a68f)

- Gender ratio
  ![image](https://github.com/user-attachments/assets/ee16bb26-1689-427c-bb59-e44329c9c8ad)







  
