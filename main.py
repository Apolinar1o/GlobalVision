import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Load the JSON files
accounts = pd.read_json('accounts_anonymized.json')
cases = pd.read_json('support_cases_anonymized.json')

# Explore the datasets
print("Accounts Dataset:")
print(accounts.head())

print("\nSupport Cases Dataset:")
print(cases.head())

# Connect to SQLite database
conn = sqlite3.connect('support_analysis.db')
cursor = conn.cursor()

# Create tables in the database
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    account_sfid TEXT PRIMARY KEY,
    account_name TEXT,
    account_country TEXT,
    account_industry TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cases (
    case_id TEXT PRIMARY KEY,
    case_number TEXT,
    case_status TEXT,
    account_sfid TEXT,
    FOREIGN KEY (account_sfid) REFERENCES accounts (account_sfid)
)
''')

# Insert data into tables
accounts.to_sql('accounts', conn, if_exists='replace', index=False)
cases.to_sql('cases', conn, if_exists='replace', index=False)

# Clean and transform data using SQL
cursor.execute('''
UPDATE accounts
SET account_country = 'Unknown'
WHERE account_country IS NULL
''')

cursor.execute('''
UPDATE accounts
SET account_industry = 'Unknown'
WHERE account_industry IS NULL
''')

cursor.execute('''
DELETE FROM cases
WHERE account_sfid IS NULL
''')

# Join the datasets based on account_sfid
merged_data = pd.read_sql_query('''
SELECT cases.*, accounts.account_name, accounts.account_country, accounts.account_industry
FROM cases
JOIN accounts ON cases.account_sfid = accounts.account_sfid
''', conn)

print("\nMerged Data:")
print(merged_data.head())

# Part 3: Data Visualization
# Count the number of cases per account
cases_per_account = merged_data.groupby('account_sfid').size().reset_index(name='TotalCases')
print("\nTotal Cases per Account:")
print(cases_per_account.head())

# Analyze the status of cases
status_analysis = merged_data['case_status'].value_counts()
print("\nCase Status Analysis:")
print(status_analysis)

# Improve Bar Chart: Number of Cases per Account
plt.figure(figsize=(15, 8))
cases_per_account = cases_per_account.sort_values(by='TotalCases', ascending=False)
top_n = 15  # Show the top 15 accounts with the most cases
cases_per_account_top = cases_per_account.head(top_n)

plt.bar(cases_per_account_top['account_sfid'], cases_per_account_top['TotalCases'], color='skyblue')
plt.title("Number of Cases per Account", fontsize=16)
plt.xlabel("account_sfid", fontsize=12)
plt.ylabel("Total Cases", fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)  # Adjust the rotation and font size
plt.tight_layout()
plt.show()

# Pie Chart: Distribution of Case Statuses
threshold = 0.02
filtered_status = status_analysis[status_analysis / status_analysis.sum() > threshold]
other_status = status_analysis[status_analysis / status_analysis.sum() <= threshold].sum()
filtered_status['Other'] = other_status

plt.figure(figsize=(8, 8))
filtered_status.plot(kind='pie', autopct='%1.1f%%', startangle=140, title="Distribution of Case Statuses")
plt.ylabel("")
plt.legend(title='Status')
plt.tight_layout()
plt.show()

# Part 4: Business Insights
print("\nDerived Insights:")
print("- Accounts with the most cases can be prioritized for support.")
print("- The most common status may indicate recurring issues or delays in resolution.")

print("\nAction Proposals:")
print("1. Implement a tracking system for accounts with the most cases.")
print("2. Review processes for the most common case statuses to optimize resolution.")

# Close the database connection
conn.close()
