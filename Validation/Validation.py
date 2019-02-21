import pandas as pd
df = pd.read_fwf("A320_SLC1_mod.rpt", skiprows=[1])

headers = list(df.columns.values)
ValueMatrix = []

for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    ValueMatrix.append(dfList)
    
#headers.index(header) to recall corresponding list in ValueMatrix
Misestress = []
iteration = 0
for miseone in ValueMatrix[2]:
    misetwo = ValueMatrix[3][iteration]
    iteration = iteration + 1
    MiseStressAvg = (float(miseone) + float(misetwo))/2
    Misestress.append(MiseStressAvg)

print Misestress
