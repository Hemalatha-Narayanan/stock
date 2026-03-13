import _json
import datetime as dt
import pandas as pd
import requests
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
github_api_url="https://api.github.com/repos/squareshift/stock_analysis/contents/"
response=requests.get(github_api_url)
print(response)
#print(response.text) #in string format unaligned cannot be iterable
b=response.json()  # organised and can be iterable using index
#print( "Json fromat:",b)
csv_files=[f['download_url'] for f in b if f['name'].endswith('.csv')]
#print("downloadable url:",len(csv_files),csv_files) #display total url:21 and link
csv_file=csv_files.pop() #last url only contains Meta data
#print("Fetch Last Url contains Meta data:",csv_file)
d=pd.read_csv(csv_file) #contains only meta data
#print(d)
#print(type(d))
dataframe=[]
filename=[]
for url in csv_files:
    filenames=url.split("/")[-1].replace(".csv","")
    #print("Filename:",filenames)
    df=pd.read_csv(url)
    #print("df:",df)
    df['Symbol']=filenames
    #print(df['Symbol'])
    dataframe.append(df)
    filename.append(filenames)
    #print(filename)
    #print(dataframe)

combined_df = pd.concat(dataframe, ignore_index=True) #here align datas inside dataframe using [pd.concat] pandas used for data processing
#print(combined_df)
o_df = pd.merge(combined_df,d,on='Symbol',how='left')
#print(o_df)
result=o_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
#print(result)
o_df["timestamp"]=pd.to_datetime(o_df['timestamp'])
#print(o_df)
filtered_df=o_df[(o_df['timestamp'] >= "2021-01-01") & (o_df['timestamp'] <= "2021-05-26")]
res_time=filtered_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
#print(res_time)
list_sector=["TRADE & SERVICES","LIFE SCIENCES"]
res_time = res_time[res_time["Sector"].isin(list_sector)].reset_index(drop=True)
print(res_time)
path=r"C:\Users\rd070\OneDrive\Desktop\Data Engineering\stock analysis.csv"
res_time.to_csv(path,index=True)
print("Poc Completed")
