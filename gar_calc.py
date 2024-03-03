import pandas as pd
import json
import re

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
customer_exposure = pd.read_csv('customer_exposure.csv', delimiter=';')

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
