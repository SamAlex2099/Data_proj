
import pandas as pd
import numpy as np


file_path = '/Users/samuelalexander/Desktop/Copy of Copy of SRTS Cartage Report- 2024 -June.xlsx'
sheetname = input("Enter sheet name or index (leave blank for the first sheet):")
facility = input("Enter facility name:")
weekending= input("Enter the week ending date e.g. dd/mm/yyyy:")


#input file path
def load_excel_file(file_path, sheetname, header_row = 3):
    if sheetname.isdigit():
        sheetname = int(sheetname)

    elif sheetname == "":
        sheetname = 0

    df = pd.read_excel(file_path, sheet_name=sheetname, header=header_row)

    return df

df = load_excel_file(file_path, sheetname)

df = df.dropna(subset=['Description'])  # Remove NaN values
df = df[df['Description'].str.strip() != '']  # Remove empty strings


print("Columns in DataFrame:", df.columns.tolist())
print("First few rows of the DataFrame:")
print(df.head())

if df is not None:
    new_columns = ['FACILITY','WEEK-ENDING','EQUIPMENT TYPE','EQUIPMENT ID','WEEK (HRS)','TOTAL (HRS)','MILEAGE (KMS)','TOTAL (KMS)','STATUS']
    new_df = pd.DataFrame(columns = new_columns )
    #to iterate over rows in description column
    hours_key = ['cat','jcb','bell','loader','end','front','compactor','tanker','dozer','dumper','excavator','bomag','dezzi']

    for index,row in df.iterrows():
        description = row['Description']
        

        #initialize values
        mileage = None
        hours = None
        total_kms = None
        total_hrs = None
       

        if pd.notna(description) and description.strip():
            if  isinstance(description, str) and any(key in description.lower() for key in hours_key):
                hours = row['Finish']
                total_hrs = row['Total']
            elif isinstance(description, str):
                mileage = row['Finish']
                total_kms = row['Total']
        
        status = row['Finish'] - row['Start']

        if status > 0:
            status = 'Operational'
        else:
            status = 'Non-Operational'

        # Create a new row DataFrame for the current iteration
        row_addition = pd.DataFrame({
            'FACILITY':[facility],
            'WEEK-ENDING': [weekending],
            'EQUIPMENT TYPE': [description],
            'EQUIPMENT ID': [row['Equipment No.']],
            'WEEK (HRS)': [total_hrs],
            'TOTAL (HRS)': [hours],
            'MILEAGE (KMS)': [total_kms],
            'TOTAL (KMS)': [mileage],
            'STATUS': [status]
        })

        # Append the new row DataFrame to new_df
        new_df = pd.concat([new_df, row_addition], ignore_index=True)
        new_df= new_df.fillna('null')
        new_df["EQUIPMENT ID"] = new_df["EQUIPMENT ID"].replace('null', str(''))
        new_df = new_df.replace(0,'null')
        new_df = new_df.replace(',','.',regex= True)


new_df.to_excel('/Users/samuelalexander/Desktop/New_DataFrame.xlsx', index=False)
print(f"New DataFrame created and saved.")
print(new_df.head())