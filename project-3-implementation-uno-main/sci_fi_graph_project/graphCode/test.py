# # import os
# # import pandas as pd

# # def get_subreddit_name(file_name):
# #     return os.path.splitext(file_name)[0]

# # def create_subreddit_dict(directory_path):
# #     all_files = os.listdir(directory_path)
    
# #     # Create an empty dictionary to store the data
# #     subreddit_dict = {}

# #     for file_name in all_files:
# #         if file_name.endswith('.csv'):
# #             file_path = os.path.join(directory_path, file_name)
# #             df = pd.read_csv(file_path)

# #             # Extract 'subreddit' name
# #             subreddit_name = get_subreddit_name(file_name)
# #             print(subreddit_name)

# #             # Create a dictionary entry with 'subreddit' as key
# #             if subreddit_name not in subreddit_dict:
# #                 subreddit_dict[subreddit_name] = []

# #             # Add a tuple of ('subredditSubscribers', 'fileName') to the list
# #             subreddit_dict[subreddit_name].append((df['subredditSubscribers'].iloc[0], df['dataCollectionDate'].iloc[0]))

# #     return subreddit_dict

# # if __name__ == "__main__":
# #     directory_path = './Reddit/subscribers/'

# #     # Create a dictionary of subreddit data
# #     subreddit_data_dict = create_subreddit_dict(directory_path)

# #     # Print the resulting dictionary
# #     for subreddit, data_list in subreddit_data_dict.items():
# #         print(f"Subreddit: {subreddit}")
# #         for data in data_list:
# #             print(f"  Subreddit Subscribers: {data[0]}, File Name: {data[1]}")

# import os
# import pandas as pd

# # Directory containing CSV files
# directory_path = './Reddit/hateComments/'

# # Get a list of all files in the directory
# file_list = os.listdir(directory_path)

# # Filter for CSV files
# csv_files = [file for file in file_list if file.endswith('.csv')]

# # Initialize an empty list to store DataFrames for each CSV file
# dfs = []
# user_ids = []
# bodies = []

# # Iterate over CSV files and read each into a DataFrame
# for csv_file in csv_files:
#     file_path = os.path.join(directory_path, csv_file)
#     df = pd.read_csv(file_path)

#     total_hate = df['HateSpeech'].sum()
#     new_df = pd.DataFrame({
#         'date': [csv_file.replace('.csv', '')],
#         'count': [len(df)],
#         'totalHate': [total_hate]
#     })
#     dfs.append(new_df)
    
#     df = pd.read_csv(file_path)
#     hate_speech_rows = df[df['HateSpeech'] == True]
#     user_ids.extend(hate_speech_rows['userID'].tolist())
#     bodies.extend(hate_speech_rows['body'].tolist())

# # Concatenate all DataFrames into a single DataFrame
# result_df = pd.concat(dfs, ignore_index=True)

# # Print the result DataFrame
# print(result_df)
# print("User ID DataFrame:")
# print(len(user_ids))

# print("\nBody DataFrame:")
# print(len(bodies))
