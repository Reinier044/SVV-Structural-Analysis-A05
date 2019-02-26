import pandas as pd
filename = raw_input("file name (no need to give csv extension): ")
df = pd.read_csv(str(filename+".csv"))

headers = list(df.columns.values)   #create list of all column (header) names
dataset = {}                        #create empty dictionary for all data

flag = 0                            #Set flag to skip first empty column
for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    if flag>0:
        dataset[header]=dfList      #Create dictionary item with header as its key and returns a list containing all datapoints
    flag = flag + 1                       #Used to not write the first empty column in the dataset 

Small = 0
for i in dataset['x']:
    print i