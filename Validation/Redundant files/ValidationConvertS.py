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
while i<=1:
    dataset[headers[i]]=ValueMatrix[i]
    i = i + 1

#headers.index(header) to recall corresponding list in ValueMatrix
Misestress = []
iteration = 0
for miseone in ValueMatrix[2]:
    misetwo = ValueMatrix[3][iteration]
    iteration = iteration + 1
    try:
        MiseStressAvg = (float(miseone) + float(misetwo))/2     #average the von mises stress of upper and lower side
    except:
        MiseStressAvg = 'nan'               #to avoid errors
    Misestress.append(MiseStressAvg)

#Write new csv file with average von Mises stress for each node
dataset['MiseStress']=Misestress
newdf = pd.DataFrame(data=dataset)
newdf.to_csv(str(filename+'.csv'))
