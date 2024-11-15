import pandas as pd
import requests
import logging
from time import sleep
import re
from tqdm import tqdm

logging.basicConfig(filename='processing_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


def clean_newlines(text):
    # Replace consecutive newline characters with a single space
    cleaned_text = re.sub(r'\n+', ' ', text)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
    return cleaned_text

def hs_check_comment(comment):
    # sleep(0.5)
    CONF_THRESHOLD = 0.9

    data = {
        "token": "193e6a97891628d85afb65362bcf7452",
        "text": clean_newlines(comment.strip())
    }

    response = requests.post("https://api.moderatehatespeech.com/api/v1/moderate/", json=data).json()
    # print(response)

    if response["response"] == "Success":
        if response["class"] == "flag" and float(response["confidence"]) > CONF_THRESHOLD:
            return True
        return False
    else:
        print("Sleeping")
        sleep(1)
    return "ERROR"

# Replace 'reddit.txt' with the path of your file containing the list of CSV files
file_list_path = 'politics.txt'

# Read the file paths from reddit.txt
with open(file_list_path, 'r') as file:
    file_paths = file.read().splitlines()

lenFilePath = len(file_paths)

# Loop through each file path and apply the hs_check_comment function
for i in tqdm(range(len(file_paths)), desc="Processing Files", unit="file"):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_paths[i])

        # Apply the hs_check_comment function to the "Body" column and store the results in a new "HateSpeech" column
        df['HateSpeech'] = df['body'].apply(hs_check_comment)

        # Save the DataFrame back to the same CSV file
        df.to_csv(file_paths[i], index=False)

        logging.info(f'Successfully processed and updated: {file_paths[i]}')
    except Exception as e:
        logging.error(f'Error processing file {file_paths[i]}: {str(e)}')

print('Processing complete. Check processing_log.txt for details.')
