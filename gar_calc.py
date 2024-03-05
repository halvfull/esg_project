import pandas as pd
import json
import re
import sys
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Customers, Base


sys.path.append('./')
# Function to read a JSON file and return its contents
def read_json(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        return json.load(file)

# Read in the taxonomy data from a JSON file
file_path = 'taxonomy.json'
taxonomy_data = read_json(file_path=file_path)
activities = taxonomy_data['activities']
taxonomy = pd.json_normalize(activities)

# Read in the customer exposure data from a CSV file
#Update path to reflect your own CSV.
customer_exposure = pd.read_csv('/Users/jakobsterri/esg_project/esg_project/customer_exposure.csv', delimiter=';')

# Normalize the taxonomy NACE codes by removing all chars and periods, considering multiple codes
taxonomy['nace_normalized'] = taxonomy['nace_codes'].apply(
    lambda x: [re.sub(r'[^\d]', '', code) for code in x.split(',')] if pd.notnull(x) else []
)

# Flatten the list of normalized NACE codes into a set of unique codes
taxonomy_nace_flat = set()
for sublist in taxonomy['nace_normalized']:
    for item in sublist:
        taxonomy_nace_flat.add(item)

# Prepare the customer_exposure data
# Ensure that we remove any non-digit characters from the NACE codes, considering the first four digits
customer_exposure['nace_level_4'] = customer_exposure['nace'].astype(str).apply(
    lambda x: re.sub(r'[^\d]', '', x)[:4]
)

# Determine eligibility based on the normalized NACE codes
customer_exposure['is_green'] = customer_exposure['nace_level_4'].apply(
    lambda x: x in taxonomy_nace_flat
)


Base.metadata.create_all(bind=engine)

def load_customers(df: pd.DataFrame):
    db = SessionLocal()
    try:
        for index, row in df.iterrows():
            # Convert the 'nace' column value to string and apply regex, ensuring it's not NaN/None
            nace_as_str = str(row['nace']) if pd.notnull(row['nace']) else '0'
            nace_cleaned = int(re.sub(r'[^\d]', '', nace_as_str))
            
            new_customer = Customers(
                year_month=int(row['year_month']),
                customerno=row['customerno'],
                customername=row['customername'],
                countrycd=row['countrycd'],
                nace=nace_cleaned,  # Use the cleaned, integer-converted 'nace' value
                currencycd=row['currencycd'],
                total_exposure=float(row['total_exposure']),
                nace_level_4=row['nace_level_4'],
                is_green=bool(row['is_green'])
            )
            db.add(new_customer)
        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()



def load_customers_to_db(df, engine):
    df.to_sql('customers', con=engine, if_exists='append', index=False, chunksize=500)

# Call the function with the prepared DataFrame and the engine
load_customers_to_db(customer_exposure, engine)

# Load the prepared DataFrame into the database
#load_customers(customer_exposure)