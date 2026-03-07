import json
import datetime as dt
import requests
import pandas as pd
import pandas as pd
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
github_api_url = "https://api.github.com/repos/squareshift/stock_analysis/contents/"
response = requests.get(github_api_url)
# print(response)
# print(response.status_code)
b = response.json()
# a = response.text
# print(a)
# print(b)
csv_files = [file['download_url'] for file in b if file['name'].endswith('.csv')]

csv_file = csv_files.pop()
# print(csv_file)
d = pd.read_csv(csv_file)
# print(d)
# print(type(d))
dataframes=[]
file_names=[]
for url in csv_files:
    file_name = url.split("/")[-1].replace(".csv", "")
    # print(file_name)

    df = pd.read_csv(url)
    # print(df)
    df['Symbol'] = file_name
    # print(df['Symbol'])
    dataframes.append(df)
    # print(dataframes)
    file_names.append(file_name)

combined_df = pd.concat(dataframes, ignore_index=True)
# print(combined_df)
o_df = pd.merge(combined_df,d,on='Symbol',how='left')
# print(o_df)
result = o_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
# print(result)

o_df["timestamp"] = pd.to_datetime(o_df["timestamp"])
# print(o_df["timestamp"])
filtered_df = o_df[(o_df['timestamp'] >= "2021-01-01") & (o_df['timestamp'] <= "2021-05-26")]
result_time = filtered_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
# print(result_time)
list_sector = ["TECHNOLOGY","FINANCE"]
result_time = result_time[result_time["Sector"].isin(list_sector)].reset_index(drop=True)
print(result_time)
path = r"C:\Users\Deepika Mohan\OneDrive\Documents\stock_data.csv"
result_time.to_csv(path, header=True)
print('data saved sucessfully')