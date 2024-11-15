import os
import pandas as pd

# Specify the directory containing your CSV files
directory_path = './News'

# Create an empty dictionary to store dateOfCreation: total_rows pairs
data_summary = {}

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory_path, filename)

        # Extract dateOfCreation from the filename
        date_of_creation = filename.replace('.csv', '')

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Get the total number of rows
        total_rows = len(df)

        # Update the dictionary with dateOfCreation and total_rows
        data_summary[date_of_creation] = total_rows

# Convert the dictionary to a pandas DataFrame
summary_df = pd.DataFrame(list(data_summary.items()), columns=['dateOfCreation', 'total_rows'])

# Display the resulting table
print(summary_df)
