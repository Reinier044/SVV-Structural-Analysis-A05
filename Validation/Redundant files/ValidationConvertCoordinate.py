import pandas as pd
filename = 'Coordinates'
df = pd.read_fwf(str("Coordinates.rpt"), skiprows=[1])

headers = list(df.columns.values)
ValueMatrix = []

for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    ValueMatrix.append(dfList)

dataset = {}
i = 0
while i<=1:
    dataset[headers[i]]=ValueMatrix[i]
    i = i + 1

#headers.index(header) to recall corresponding list in ValueMatrix
df.to_csv(str(filename+'.csv'))