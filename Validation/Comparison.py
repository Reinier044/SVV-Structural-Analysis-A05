import pandas as pd
name = raw_input("Loadcase code: ")
filenameInput = 'A320_Comp_'+name+'.csv'

df = pd.read_csv(filenameInput)
print 
print "//Imported data"

headers = list(df.columns.values)   #create list of all column (header) names. Should produce ['Index', 'MiseStress', 'U.Mag', 'U.U1', 'U.U2', 'U.U3', 'x', 'y', 'z']

dataset = {}                        #create empty dictionary for all data

flag = 0                            #Set flag to skip first empty column
for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    dataset[header]=dfList      #Create dictionary item with header as its key and returns a list containing all datapoints
    flag = flag + 1                       #Used to not write the first empty column in the dataset 


