import pandas as pd
name = raw_input("Loadcase code: ")
filenameStress = 'A320_S'+name+'.csv'
filenameDefl = 'A320_U'+name+'.csv'
filenamOutput = 'A320_Val_'+name+'.csv'
filenameCoor = 'Coordinates.csv'
df = pd.read_csv(str(filenameCoor))
print 
print "//Started reformatting nodes of discretization"


#Lengths of aileron
Lx = 2771
Lz = 547
Ly = 112.5

#-----------------------------------------------------------------------------------------------------
headers = list(df.columns.values)   #create list of all column (header) names
dataset = {}                        #create empty dictionary for all data

for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    dataset[header]=dfList      #Create dictionary item with header as its key and returns a list containing all datapoints


Xcoors = []              #create list with edging coordinates of discretization segments in x
primer = 0              #Create integer that runs through the length of the aileron per centimeter
while primer<(Lx+1):
    occurences = 0
    for i in dataset['x']:
        if int(i) == primer:          #check if the primer occurs as a discretization coordinate
            occurences = occurences + 1
    if occurences> 0:
        Xcoors.append(primer)       #add the discretization coordinate to the list
    primer = primer + 1

#Create lists that contain the new counting order
NewNode = []
NewX = []
NewY = []
NewZ = []


for segment in Xcoors:       
    primer = 0          #Index number of discretization segment
    
    #Create lists for temporary storage of partly ordered segments
    Temp1Node = []
    Temp1X = []
    Temp1Y = []
    Temp1Z = []
    
    IndexList = []
    while len(IndexList)<58:
        if int(dataset['x'][primer]) == segment:  #If the primer corresponds to the Coordinate we are checking for, append the corresponding index to the indexlist 
            IndexList.append(primer)
        elif primer == (len(dataset['x'])-1):       #Add a break for errors due to odd discretizations
            break
        primer = primer + 1
        
    for value in IndexList:                         #Append Coordinates to temporary list for next ordering algorithm
        Temp1Node.append(dataset['node'][value])
        Temp1X.append(dataset['x'][value])
        Temp1Y.append(dataset['y'][value])
        Temp1Z.append(dataset['z'][value])
    
    #Create lists for temporary storage of partly ordered segments
    Temp2Node = []
    Temp2X = []
    Temp2Y = []
    Temp2Z = []
    
    #The algorithm picks the largest remaining number from the list and stores it in the temporary list for each segment
    while len(Temp1Z)>0:
        ZcheckValue = 0             #Number that increases when a higher number is found
        primer = 0                  #Primer runs through the whole list. Increases by 1 each iteration
        index = 0                   #Stored index number of the Zcheckvalue
        while primer<len(Temp1Z):
            if Temp1Z[primer] > ZcheckValue:
                ZcheckValue = Temp1Z[primer]    #Store the numer if it proves to be higher than previous iteration
                index = primer              #Store the primer (index number) of the current highest found number in the list
            primer = primer + 1
        ZcheckValue = 0
        
        #Append the highest valued found node and delete it from the old list
        Temp2Node.append(Temp1Node[index])
        Temp2X.append(Temp1X[index])
        Temp2Y.append(Temp1Y[index])
        Temp2Z.append(Temp1Z[index])
        del Temp1Node[index]
        del Temp1X[index]
        del Temp1Y[index]
        del Temp1Z[index]
    
    #Append the list for the current segment to the master list that is outside of the loop
    NewNode = NewNode + Temp2Node
    NewX = NewX + Temp2X
    NewY = NewY + Temp2Y
    NewZ = NewZ + Temp2Z

#Create new dict for the new coordinate data
Coordataset = {}

Coordataset['node'] = NewNode
Coordataset['x']= NewX
Coordataset['y']= NewY
Coordataset['z']= NewZ

print
print '//Finished reformatting'


#--------------------------------------------------------------------------------------------------------

#Import the stress data    
df = pd.read_csv(str(filenameStress))
print
print '//Started linking stress data to nodes'


headers = list(df.columns.values)   #create list of all column (header) names
Stressdataset = {}                        #create empty dictionary for all data

for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    Stressdataset[header]=dfList      #Create dictionary item with header as its key and returns a list containing all datapoints



#Create lists that contain the new counting order
NewNode = []
NewX = []
NewY = []
NewZ = []
NewStress = []

Coorprimer = 0                      #Set primer that runs through all the Coordinate nodes list
for node in Coordataset['node']:
    Stressprimer = 0                #Set primer that runs through all the stress nodes list
    
    #Append current node information to the lists
    NewNode.append(node)
    NewX.append(Coordataset['x'][Coorprimer])
    NewY.append(Coordataset['y'][Coorprimer])
    NewZ.append(Coordataset['z'][Coorprimer])
    Stress = 0
    
    #Look for the Von Mises stress of the current node
    while Stressprimer < len(Coordataset['node']):
        if int(Stressdataset['Node'][Stressprimer]) == int(node):       #Check if node corresponds to node in the stress file
        
            #If node corresponds, change Stress value accordingly
            Stress = Stressdataset['MiseStress'][Stressprimer]
            break
        else:
            Stressprimer = Stressprimer + 1
    #Append stress value to the list
    NewStress.append(Stress)
    Coorprimer = Coorprimer + 1

print
print '//Finished linking stress data'

#-------------------------------------------------------------------------------------------
    
    
#Import the Deflection data    
df = pd.read_csv(str(filenameDefl))

print
print '//Started linking deflection data to nodes'


headers = list(df.columns.values)   #create list of all column (header) names
Defldataset = {}                        #create empty dictionary for all data

for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    Defldataset[header]=dfList      #Create dictionary item with header as its key and returns a list containing all datapoints



#Create lists that contain the new counting order
UMag = []
U1 = []
U2 = []
U3 = []


Nodeprimer = 0                      #Set primer that runs through all the Coordinate nodes list
for node in Coordataset['node']:
    Deflprimer = 0                #Set primer that runs through all the deflection nodes list   
    uMag = 0
    u1 = 0
    u2 = 0
    u3 = 0
    while Deflprimer < len(Coordataset['node']):
        if int(Defldataset['Node'][Deflprimer]) == int(node):       #Check if node corresponds to node in the deflection file
        
            #Append all the data for the found node with the corresponding index to the new lists 
            uMag = Defldataset['U.Mag'][Deflprimer]
            u1 = Defldataset['U.U1'][Deflprimer]
            u2 = Defldataset['U.U2'][Deflprimer]
            u3 = Defldataset['U.U1'][Deflprimer]
            break
        else:
            Deflprimer = Deflprimer + 1
            
    UMag.append(uMag)
    U1.append(u1)
    U2.append(u2)
    U3.append(u3)
    Nodeprimer = Nodeprimer + 1

print
print '//Finished linking deflection data'

#---------------------------------------------------------------------------------------------

#Put all data in a dictionary
Finaldataset = {}

Finaldataset['node'] = NewNode
Finaldataset['x']= NewX
Finaldataset['y']= NewY
Finaldataset['z']= NewZ
Finaldataset['MiseStress'] = NewStress
Finaldataset['U.Mag'] = UMag
Finaldataset['U.U1'] = U1
Finaldataset['U.U2'] = U2
Finaldataset['U.U3'] = U3

#Write new dataset to the csv file
newdf = pd.DataFrame(Finaldataset)
newdf.to_csv(filenamOutput)

print
print '//Finished. Written data into:'
print filenamOutput


