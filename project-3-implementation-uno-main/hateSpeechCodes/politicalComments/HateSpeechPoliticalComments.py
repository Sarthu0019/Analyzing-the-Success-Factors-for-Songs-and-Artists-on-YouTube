import pandas as pd
import requests
import logging
from time import sleep
import re
from tqdm import tqdm

logging.basicConfig(filename='processing_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


def clean_newlines(text):
    cleaned_text = re.sub(r'\n+', ' ', text)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
    return cleaned_text

def hs_check_comment(comment):
    CONF_THRESHOLD = 0.9

    data = {
        "token": "193e6a97891628d85afb65362bcf7452",
        "text": clean_newlines(comment.strip())
    }

    response = requests.post("https://api.moderatehatespeech.com/api/v1/moderate/", json=data).json()

    if response["response"] == "Success":
        if response["class"] == "flag" and float(response["confidence"]) > CONF_THRESHOLD:
            return True
        return False
    else:
        print("Sleeping")
        sleep(1)
    return "ERROR"

file_list_path = 'politics.txt'

with open(file_list_path, 'r') as file:
    file_paths = file.read().splitlines()

lenFilePath = len(file_paths)

for i in tqdm(range(len(file_paths)), desc="Processing Files", unit="file"):
    try:
        df = pd.read_csv(file_paths[i])

        df['HateSpeech'] = df['body'].apply(hs_check_comment)

        df.to_csv(file_paths[i], index=False)

        logging.info(f'Successfully processed and updated: {file_paths[i]}')
    except Exception as e:
        logging.error(f'Error processing file {file_paths[i]}: {str(e)}')

print('Processing complete. Check processing_log.txt for details.')
