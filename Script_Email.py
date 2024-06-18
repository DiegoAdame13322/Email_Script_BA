import csv
from datetime import datetime

# Define paths to ADA_CNP data files
ada_cnp_files = [
    'Files/ADA_CNP.txt',
    'Files/ADA_CNP_FL.txt',
    'Files/ADA_CNP_LA.txt',
    'Files/ADA_CNP_MIDLAND.txt',
    'Files/ADA_CNP_OH.txt'
]

# Function to load ADA_CNP data from multiple files into one list
def load_ada_cnp_files(files):
    all_data = []
    for file_path in files:
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                # Standardize date format
                row['ATTDATE'] = standardize_date(row['ATTDATE'])
                # Convert membership and absences to integers
                row['MEMBERSHIP'] = int(row['MEMBERSHIP'])
                row['ABSENCES'] = int(row['ABSENCES'])
                # Calculate attendance
                row['ATTENDANCE'] = row['MEMBERSHIP'] - row['ABSENCES']
                all_data.append(row)
    return all_data

# Function to standardize date format
def standardize_date(date_str):
    formats_to_try = ['%d-%b-%y', '%m/%d/%Y']
    for format_str in formats_to_try:
        try:
            return datetime.strptime(date_str, format_str).strftime('%m/%d/%Y')
        except ValueError:
            continue
    return date_str  # Return original if no format matches

# Load all ADA_CNP data into one list
ada_cnp_data = load_ada_cnp_files(ada_cnp_files)
#print(ada_cnp_data)

# Define the path to the SalesData.csv file
sales_data_file = 'Files/SalesData.csv'
def load_sales_data(file_path):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        for entry in data:
            # Combine 'Campus' and 'Site' into 'School Name'
            entry['School Name'] = f"{entry['Campus']} {entry['Site']}"
            # Format 'SaleDate' to have leading zeros for months
            month, day, year = entry['SaleDate'].split('/')
            entry['SaleDate'] = f"{month.zfill(2)}/{day}/{year}"
    return data

# Load SalesData.csv into a list of dictionaries
sales_data = load_sales_data(sales_data_file)

# List to store non-compliant records
non_compliant_records = []

# Iterate through SalesData and compare with ada_cnp_data
for entry in sales_data:
    school_name = entry['School Name']
    sale_date = entry['SaleDate']
    meal_type = entry['MealType']
    free_count = int(entry['FreeCount'])

    # Find matching ADA_CNP entry based on school name and sale date
    matched_entries = [data for data in ada_cnp_data if data['SCHOOLNAME'] == school_name and data['ATTDATE'] == sale_date]

    if matched_entries:
        for matched_entry in matched_entries:
            attendance = matched_entry['ATTENDANCE']
            if free_count > attendance:
                meals_over = free_count - attendance
                non_compliant_records.append({
                    'School Name': school_name,
                    'Sale Date': sale_date,
                    'Meal Type': meal_type,
                    'Free Count': free_count,
                    'Attendance': attendance,
                    'Meals Over': meals_over
                })
    # else:
    #     print(f"No matching ADA_CNP data for School Name: {school_name}, Sale Date: {sale_date}")

# Print out non-compliant records
print("\nNon-Compliant Records:")
for record in non_compliant_records:
    print(f"School Name: {record['School Name']}")
    print(f"Sale Date: {record['Sale Date']}")
    print(f"Meal Type: {record['Meal Type']}")
    print(f"Total Count: {record['Free Count']}")
    print(f"Attendance: {record['Attendance']}")
    print(f"Meals Over: {record['Meals Over']}")
    print("")
