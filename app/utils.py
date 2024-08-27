import pandas as pd
from datetime import datetime, date

def validate_excel(file):
    errors = []
    df = pd.read_excel(file)

    # Checking if all the columns are present
    required_columns = ['Sno', 'FirstName', 'LastName', 'Gender', 'DateofBirth']
    for col in required_columns:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")

    # Validate each row
    for index, row in df.iterrows():
        # Validate Sno
        sno_str = str(row['Sno']) if not pd.isna(row['Sno']) else None
        if not sno_str or sno_str in df['Sno'].astype(str)[:index].values:   #check if sno_str present in the sno(the start of the DF up to the current row)
            errors.append(f"Row {index + 1}: 'Sno' must be a unique string.")   #since DF index starts from 0

        # Validate FirstName and LastName
        if pd.isna(row['FirstName']) or not isinstance(row['FirstName'], str) or not (0 < len(row['FirstName']) <= 50):  #if its NaN/str/<50
            errors.append(f"Row {index + 1}: 'FirstName' must be a string with length between 1 and 50.")
        if pd.isna(row['LastName']) or not isinstance(row['LastName'], str) or not (0 < len(row['LastName']) <= 50):
            errors.append(f"Row {index + 1}: 'LastName' must be a string with length between 1 and 50.")

        # Validate Gender
        if pd.isna(row['Gender']) or row['Gender'] not in ['M', 'F', 'O']:
            errors.append(f"Row {index + 1}: 'Gender' must be 'M', 'F', or 'O'.")


# Validate DOB
    df['DateofBirth'] = df['DateofBirth'].astype(str)

    for index, row in df.iterrows():
        # Validate DateofBirth
        dob_str = str(row['DateofBirth']).strip()     #remove whitespace if any!

        # Check if the date is in the correct format (YYYY-MM-DD)
        if len(dob_str) != 10 or dob_str[4] != '-' or dob_str[7] != '-':
            errors.append(f"Row {index + 1}: 'DateofBirth' must be in YYYY-MM-DD format.")
        else:
            try:
                # Convert the string to a date object
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()     #converting date string into a date object

                # Check if the date is in the future
                if dob >= datetime.now().date():
                    errors.append(f"Row {index + 1}: 'DateofBirth' must be a past date.")
                # elif(datetime.now().date()-dob).days /365 <18:
                #     errors.append(f"{index + 1}: 'DateofBirth' must be a past date.")

                else:
                    # Update the DataFrame with the date object if it's valid
                    df.at[index, 'DateofBirth'] = dob
            except ValueError:
                errors.append(f"Row {index + 1}: 'DateofBirth' must be in YYYY-MM-DD format.")


    
        # Check unique constraint for combination of 'Sno' and 'FirstName'
        if pd.isna(row['Sno']) or pd.isna(row['FirstName']):  #skips when Sno or FirstName is missing
            continue 
        if (row['Sno'], row['FirstName']) in df[['Sno', 'FirstName']].iloc[:index].values:   #check if Sno and FirstName combo already appeared previously and select all rows before the current row 
            errors.append(f"Row {index + 1}: The combination of 'Sno' and 'FirstName' must be unique.") 

    if errors:
        return False, errors, None

    return True, None, df
