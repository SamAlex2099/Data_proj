import pandas as pd

# Input parameters
#period = input("Enter the period (yyyy-mm): ")
facility_name = input("Enter the facility name: ")
file_path = input("Enter the file path to the Excel file: ")

def load_excel_file(file_path,sheet_name = 'RPTEXT'):
    # Load Excel file
    df = pd.read_excel(file_path,sheet_name)
    
    # Standardize column names: remove leading/trailing spaces and make lowercase
    df.columns = df.columns.str.strip().str.lower()
    print("Standardized column names:", df.columns)
    return df

def incoming_waste(df,facility_name):

    df['transaction date'] = pd.to_datetime(df['transaction date'])
    df['facility'] = facility_name
    df['period'] = df['transaction date'].dt.strftime('%Y-%m')

    #calculate net mass (t)

    df['quantity (t)'] = df['total netmass(kg)']/1000

    # add new column to dataframe 

    df = df[['facility', 'period','source', 'waste type', 'quantity (t)']]

    return

def outgoing_waste(df,facility_name):


    return

def beneficiation(df, facility_name):
    # Add Facility and Period columns

    df['transaction date'] = pd.to_datetime(df['transaction date'])
    df['facility'] = facility_name
    df['period'] = df['transaction date'].dt.strftime('%Y-%m')

    # Define filter criteria
    filter_types = ['commercial green (more than 1.5 ton)', 'inert waste', 'private green (less than 1.5 ton)']

    # Normalize the waste type column
    df['waste type'] = df['waste type'].str.strip().str.lower()

    # Convert filter_types to lowercase 
    normalized_filter_types = []
    for ft in filter_types:
        normalized_filter_types.append(ft.lower())

    # Debugging: Check data before filtering
    print("Unique waste types in the dataset:", df['waste type'].unique())

    # Filter and retain relevant columns
    filtered_df = df[df['waste type'].isin(normalized_filter_types)]
    print("Filtered data:\n", filtered_df)  # Debugging

    df_ben = filtered_df[['facility', 'period', 'waste type', 'net mass (t)']]
    return df_ben

try:
    # Load the Excel file
    df = load_excel_file(file_path)

    # Apply the beneficiation function
    df_ben = beneficiation(df, facility_name)

    # Print the head of the processed DataFrame
    print("Processed DataFrame:")
    print(df_ben.head())
    print("Net mass sum:",df_ben['net mass (t)'].sum())

except Exception as e:
    print(f"Error: {e}")

def diversion(df,facility_name):

     # Add Facility and Period columns

    df['transaction date'] = pd.to_datetime(df['transaction date'])
    df['facility'] = facility_name
    df['period'] = df['transaction date'].dt.strftime('%Y-%m')

     # Define filter criteria
    filter_types = ['builders rubble','clay','clean sand','coarse','fine', 'rubber waste', 'shredded tyre']

     # Normalize the waste type column
    df['waste type'] = df['waste type'].str.strip().str.lower()

     # Convert filter_types to lowercase 
    normalized_filter_types = []
    for ft in filter_types:
        normalized_filter_types.append(ft.lower())

     # Filter and retain relevant columns
    filtered_df = df[df['waste type'].isin(normalized_filter_types)]
    print("Filtered data:\n", filtered_df)  # Debugging

    df_div = filtered_df[['facility', 'period', 'waste type', 'net mass (t)']]
    return df_div




    

#/Users/samuelalexander/Downloads/VHK CC Usage Outgoing July 2023.xlsx