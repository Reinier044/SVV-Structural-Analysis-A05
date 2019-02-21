import pandas as pd
filename = raw_input("file code: ")
df = pd.read_fwf(str(filename+"_mod.rpt"), skiprows=[1])

headers = list(df.columns.values)
ValueMatrix = []

for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    ValueMatrix.append(dfList)

dataset = {}
i = 0
while i<len(headers):
    dataset[headers[i]]=ValueMatrix[i]
    i = i + 1

#headers.index(header) to recall corresponding list in ValueMatrix
newdf = pd.DataFrame(data=dataset)
newdf.to_csv(str(filename+'.csv'))