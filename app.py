from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Define your existing code as a function to process the DataFrame
def process_excel(file_path, sheetname, facility, weekending):
    # Load and clean up the DataFrame as per your original code
    df = pd.read_excel(file_path, sheet_name=sheetname, header=3)
    df = df.dropna(subset=['Description'])
    df = df[df['Description'].str.strip() != '']

    # Define the new DataFrame structure
    new_columns = ['FACILITY', 'WEEK-ENDING', 'EQUIPMENT TYPE', 'EQUIPMENT ID', 
                   'WEEK (HRS)', 'TOTAL (HRS)', 'MILEAGE (KMS)', 'TOTAL (KMS)', 'STATUS']
    new_df = pd.DataFrame(columns=new_columns)

    # Define keywords and iterate through rows for processing
    hours_key = ['cat', 'jcb', 'bell', 'loader', 'end', 'front', 
                 'compactor', 'tanker', 'dozer', 'dumper', 'excavator', 'bomag', 'dezzi']

    for index, row in df.iterrows():
        description = row['Description']
        mileage, hours, total_kms, total_hrs = None, None, None, None

        # Process rows according to your logic
        if pd.notna(description) and description.strip():
            if isinstance(description, str) and any(key in description.lower() for key in hours_key):
                hours = row['Finish']
                total_hrs = row['Total']
            elif isinstance(description, str):
                mileage = row['Finish']
                total_kms = row['Total']

        # Determine equipment status
        status = 'Operational' if (row['Finish'] - row['Start']) > 0 else 'Non-Operational'

        # Append each row to new_df
        row_addition = pd.DataFrame({
            'FACILITY': [facility],
            'WEEK-ENDING': [weekending],
            'EQUIPMENT TYPE': [description],
            'EQUIPMENT ID': [row['Equipment No.']],
            'WEEK (HRS)': [total_hrs],
            'TOTAL (HRS)': [hours],
            'MILEAGE (KMS)': [total_kms],
            'TOTAL (KMS)': [mileage],
            'STATUS': [status]
        })
        new_df = pd.concat([new_df, row_addition], ignore_index=True)

    # Clean up the final DataFrame
    new_df = new_df.fillna('null')
    new_df["EQUIPMENT ID"] = new_df["EQUIPMENT ID"].replace('null', '')
    new_df = new_df.replace(0, 'null')
    new_df = new_df.replace(',', '.', regex=True)

    return new_df

@app.route('/')
def index():
    return "Welcome to the Excel Processing API! Use POST /process-file to upload your Excel file."

@app.route('/process-file', methods=['POST'])
def process_file():
    # Get the file and other input parameters
    file = request.files['file']
    sheetname = request.form.get('sheetname')
    facility = request.form.get('facility')
    weekending = request.form.get('weekending')

    # Save the uploaded file temporarily
    file_path = os.path.join("temp", file.filename)
    file.save(file_path)

    try:
        # Convert sheetname to integer if it’s a number, else use 0 as default
        sheetname = int(sheetname) if sheetname.isdigit() else (sheetname or 0)
        
        # Call your processing function
        processed_df = process_excel(file_path, sheetname, facility, weekending)
        
        # Convert processed DataFrame to JSON for response
        result_data = processed_df.to_dict(orient='records')
        return jsonify({'status': 'success', 'data': result_data})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

    finally:
        # Clean up the temporary file
        os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
