import pandas as pd
filename = 'Coordinates'
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

newx = []
newz = []
newy = []

#Create new list with new coordinates for each node
for i in dataset['x']:
    newx.append(float(i))
for i in dataset['y']:
    newy.append(float(i))
for z in dataset['z']:
    newz.append(float(z)+float(434.5))

#Replace old lists with the new ones
dataset['x']= newx
dataset['y']= newy
dataset['z']= newz

#Write new dataset to csv file
newdf = pd.DataFrame(dataset)
newdf.to_csv(str(filename+'.csv'))

