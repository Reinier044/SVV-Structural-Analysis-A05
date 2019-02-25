name = raw_input("Loadcase code: ")
filenameInput = 'A320_Val_'+name+'.csv'

df = pd.read_csv(str(filenameInput)
print 
print "//Started reformatting nodes of discretization"

#-----------------------------------------------------------------------------------------------------
headers = list(df.columns.values)   #create list of all column (header) names
dataset = {}                        #create empty dictionary for all data

for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    dataset[header]=dfList      #Create dictionary item with header as its key and returns a list containing all datapoints

