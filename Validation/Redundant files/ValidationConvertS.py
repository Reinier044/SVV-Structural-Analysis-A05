import pandas as pd
filename = raw_input("loadcase code: ")
df = pd.read_fwf(str("A320_S"+filename+"_mod1.rpt"), skiprows=[1])

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
nodes = []
iteration = 0
thousand = 0
count = 0
node = 1
for miseone in ValueMatrix[2]:

    misetwo = ValueMatrix[3][iteration]
    iteration = iteration + 1
    try:
        MiseStressAvg = (float(miseone) + float(misetwo))/2     #average the von mises stress of upper and lower side
    except:
        MiseStressAvg = 9999              #to avoid errors
    

    nodes.append(node)
    if ((dataset['Node'][count]+thousand)<node):

        thousand = thousand + 1000
        
    node = dataset['Node'][count]+thousand
    Misestress.append(MiseStressAvg)
    count = count + 1
    if count > 5828:
        thousands = 0
        count = 0

#Write new csv file with average von Mises stress for each node
dataset['MiseStress']=Misestress
dataset['Node']=nodes
del dataset['Element']

newdf = pd.DataFrame(data=dataset)
newdf.to_csv(str("A320_S"+filename+'1.csv'))
