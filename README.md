## Automation Script for Notification of Compliance Issues

### Context

Claiming meals accurately is essential for our department to sustain and improve operations by generating revenue through state reimbursements. At the end of each month, we submit a reimbursement claim to the State, detailing Meal Counts, Membership (Enrollment), and Attendance by site. The State employs control mechanisms to identify inconsistencies and prevent fraudulent claims. However, corrections become challenging as time passes from the claim date.

### Objective

The objective of this automation script is to notify stakeholders promptly about potential days of non-compliance based on Meal Counts, Membership, Absences, and Contacts data. This proactive approach aims to enable quick corrections and ensure accurate reporting for reimbursement claims.

### Functionality

The script performs the following tasks:

1. **Data Loading and Standardization**: Loads data from various sources including ADA_CNP files and SalesData.csv. It standardizes dates and calculates attendance based on membership and absences.

2. **Comparison and Identification of Non-Compliance**: Compares Meal Counts from SalesData.csv with Attendance from ADA_CNP data. Identifies days where Meal Counts exceed Attendance, indicating potential non-compliance.

3. **Stakeholder Notification**: Automatically generates email notifications to notify stakeholders (Cafeteria Managers and Regional Managers) about non-compliant days. Emails include details such as School Name, Sale Date, Meal Type, Meal Counts, Attendance, and actionable steps for correction.

4. **Recipient Selection**: Determines the appropriate recipients for each notification based on the Job Title specified in Contacts.csv. Sends emails to Cafeteria Managers or Senior Cafeteria Managers if no Cafeteria Manager is designated. Regional Managers are CC'd for oversight.

### Example Email Content

Subject: Weekly Claim Review [Sale Date] - [Sale Date]

Body:
```
Good Morning [Recipient's First Name],

You are receiving this email because your campus had non-compliant serving days this week. Please see the serving days and meal counts below:

School Name     Meal Type     Claim Date     Meals Claimed     Attendance     Meals Over
[School Name]   [Meal Type]   [Claim Date]   [Meals Claimed]   [Attendance]   [Meals Over]

NEXT STEPS:
1. Generate a Menu Item Sales report for these dates and compare to your Counting and Claiming Excel to ensure your meal counts are accurate.
2. Verify ADA for these dates with your SIS. If your SIS has a larger number for attendance, please provide us with that documentation by replying to this email.
3. If you must edit meals, please do so before [Next Monday’s Date from Week End Date].
4. If edits are made to meal counts, be sure to update your FPRs to reflect the updated meal counts.

[Regional Manager’s Name] cc
```

### Conclusion

This automation script enhances our operational efficiency by providing timely alerts and actionable insights into potential compliance issues. By promptly notifying stakeholders, we ensure accuracy in our meal claiming process and maintain compliance with state regulations.
