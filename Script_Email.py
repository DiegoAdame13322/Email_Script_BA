import csv
from datetime import datetime

# Define paths to data files
sales_data_file = 'Files/SalesData.csv'
contacts_file = 'Files/Contacts.csv'
ada_cnp_files = [
    'Files/ADA_CNP.txt',
    'Files/ADA_CNP_FL.txt',
    'Files/ADA_CNP_LA.txt',
    'Files/ADA_CNP_MIDLAND.txt',
    'Files/ADA_CNP_OH.txt'
]


# Load CSV data into a list of dictionaries with appropriate delimiter for ADA_CNP files
def load_csv(file_path, delimiter=','):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        return list(reader)


# Standardize date format to 'YYYY-MM-DD'
def standardize_date(date_str, current_format):
    try:
        return datetime.strptime(date_str, current_format).strftime('%Y-%m-%d')
    except ValueError:
        return date_str  # Return as is if parsing fails


# Aggregate ADA_CNP data and calculate attendance
def aggregate_ada_cnp(data):
    aggregated_data = {}
    for entry in data:
        school_name_site = entry['SCHOOLNAME']  # This should contain both school name and site from the TXT file
        att_date = standardize_date(entry['ATTDATE'], '%d-%b-%y')  # Assuming 'DD-MMM-YY' format
        membership = int(entry['MEMBERSHIP'])
        absences = int(entry['ABSENCES'])
        attendance = membership - absences

        # Splitting school_name and site if they are combined
        if ' ' in school_name_site:
            parts = school_name_site.split()
            school_name = ' '.join(parts[:-1])
            site = parts[-1]
        else:
            school_name = school_name_site
            site = None  # Default to None if site is not provided in TXT file

        # Key is a tuple of school name, site, and attendance date
        key = (school_name, site, att_date)
        if key not in aggregated_data:
            aggregated_data[key] = {'Membership': 0, 'Absences': 0, 'Attendance': 0}

        aggregated_data[key]['Membership'] += membership
        aggregated_data[key]['Absences'] += absences
        aggregated_data[key]['Attendance'] += attendance

    return aggregated_data


# Load the sales and contact data (assumed to be comma-separated)
sales_data = load_csv(sales_data_file)
contacts_data = load_csv(contacts_file)

# Load the ADA_CNP data (tab-separated)
ada_cnp_data = [load_csv(file, delimiter='\t') for file in ada_cnp_files]

# Process ADA_CNP data for each file
ada_cnp_aggregated = {}
for ada_cnp_file_data in ada_cnp_data:
    aggregated_data = aggregate_ada_cnp(ada_cnp_file_data)
    ada_cnp_aggregated.update(aggregated_data)
print(ada_cnp_aggregated)
# Identify non-compliant records
non_compliant_records = []
for entry in sales_data:
    school_name = entry['Campus']
    site = entry['Site']
    date = standardize_date(entry['SaleDate'], '%m/%d/%Y')
    meal_type = entry['MealType']
    meals_claimed = int(entry['FreeCount'])

    # Create key tuple using school_name, site, and date
    key = (school_name, site, date)
    print(key)
    # Check if key exists in ada_cnp_aggregated
    if key in ada_cnp_aggregated:
        attendance = ada_cnp_aggregated[key]['Attendance']
        if meals_claimed > attendance:
            non_compliant_records.append({
                'School Name': school_name,
                'Site': site,
                'Date': date,
                'Meal Type': meal_type,
                'Meals Claimed': meals_claimed,
                'Attendance': attendance,
                'Meals Over': meals_claimed - attendance
            })
    #else:
    #    print(f"No matching ADA_CNP data for key: {key}")

# Print out non-compliant records
print("\nNon-Compliant Records:")
for record in non_compliant_records:
    school_name = record['School Name']
    site = record['Site']
    print(f"School: {school_name}")
    print(f"Site: {site}")
    print(f"Meal Type: {record['Meal Type']}")
    print(f"Claim Date: {record['Date']}")
    print(f"Meals Claimed: {record['Meals Claimed']}")
    print(f"Attendance: {record['Attendance']}")
    print(f"Meals Over: {record['Meals Over']}")
    print("")
