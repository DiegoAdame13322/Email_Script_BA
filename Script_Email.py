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
    region = entry['Region']
    campus = entry['Campus']

    # Find matching ADA_CNP entry based on school name and sale date
    matched_entries = [data for data in ada_cnp_data if
                       data['SCHOOLNAME'] == school_name and data['ATTDATE'] == sale_date]

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
                    'Meals Over': meals_over,
                    'Region': region,
                    'Campus': campus
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
    print(f"Region: {record['Region']}")
    print(f"Campus: {record['Campus']}")
    print("")

# Define path to Contacts.csv file
contacts_file = 'Files/Contacts.csv'


# Function to load contacts data from Contacts.csv
def load_contacts_data(file_path):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)


# Load Contacts.csv into a list of dictionaries
contacts_data = load_contacts_data(contacts_file)


# Function to find Regional Managers in a specific region
def find_regional_managers(region):
    regional_managers = []
    for contact in contacts_data:
        if contact['Region'] == region and contact['JobTitle'] == 'Regional Manager':
            regional_managers.append(contact)
    return regional_managers


# Function to send email to Cafeteria Managers and Regional Managers
def send_emails(non_compliant_records):
    for record in non_compliant_records:
        school_name = record['School Name']
        region = record['Region']
        campus = record['Campus']

        # Find regional managers for the current region
        regional_managers = find_regional_managers(region)

        if not regional_managers:
            print(f"No Regional Manager found for Region: {region}. Skipping email.")
            continue

        # Find Cafeteria Manager or Sr. Cafeteria Manager
        cafeteria_manager = None
        for contact in contacts_data:
            if contact['Region'] == region and contact['Campus'] == campus:
                if contact['JobTitle'] == 'Cafeteria Manager':
                    cafeteria_manager = contact
                    break
                elif contact['JobTitle'] == 'Sr. Cafeteria Manager':
                    cafeteria_manager = contact

        if not cafeteria_manager:
            print(f"No Cafeteria Manager or Sr. Cafeteria Manager found for Campus: {campus}.")
            continue

        # Construct email subject
        subject = f"Weekly Claim Review {record['Sale Date']} - {record['Sale Date']}"
        # Construct email body
        body = f"Good Morning {cafeteria_manager['Name']},\n\n"
        body += f"You are receiving this email because your campus had non-compliant serving days this week. "
        body += f"Please see the serving days and meal counts below:\n\n"
        body += f"School\tMeal Type\tClaim Date\tMeals Claimed\tAttendance\tMeals Over\n"
        body += f"{school_name}\t{record['Meal Type']}\t{record['Sale Date']}\t{record['Free Count']}\t{record['Attendance']}\t{record['Meals Over']}\n\n"
        body += "NEXT STEPS:\n"
        body += "1. Generate a Menu Item Sales report for these dates and compare to your Counting and Claiming Excel to ensure your Academy and College Prep meal counts are accurate.\n"
        body += "2. Verify ADA for these dates with your SIS. If your SIS has a larger number for attendance, please provide us with that documentation by replying to this email.\n"
        body += f"3. If you must edit meals, please do so before {record['Sale Date']}.\n"
        body += "4. If edits are made to meal counts, be sure to update your FPRs to reflect the updated meal counts.\n"
        body += f"{regional_managers[0]['Name']} cc"

        # Print or send the email here (actual email sending is not implemented here)
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print("******************************")

# Example usage:
# Assuming non_compliant_records is populated with relevant data
send_emails(non_compliant_records)
