import pandas as pd
name = raw_input("Loadcase code: ")
filenameInput = 'A320_Val_'+name+'.csv'
filenamOutput = 'A320_Comp_'+name+'.csv'

df = pd.read_csv(filenameInput)
print 
print "//Imported data"

#Seg is the term that comes from the validation model. Boom comes from the numerical method
BoomA = [103.71,103.71,103.71,103.71,103.71,103.71,103.71,182.19,129.75,106.83,129.75,182.19,103.71,103.71,103.71,103.71,103.71,103.71,103.71]
BoomZ = [54.31,108.62,162.93,217.24,271.55,325.86,380.17,434.48,514,547,514,434.48,380.17,325.86,271.55,217.24,162.93,108.62,54.31]
BoomY = [-14.0625,-28.125,-42.1875,-56.25,-70.3125,-84.375,-98.4375,-112.5,-79.55,0.0,79.55,112.5,98.4375,84.375,70.3125,56.25,42.1875,28.125,14.0625]
SegZ = [0.0, 24.138885000000002, 48.277771000000001, 72.416656000000003, 96.555542000000003, 120.69445800000001, 144.83334399999998, 168.972229, 193.11111499999998, 217.25, 241.38888500000002, 265.52777099999997, 289.66667200000001, 313.80555699999996, 337.94444269999997, 362.08333589999995, 386.22222139999997, 410.36111069999998, 434.5, 434.5, 434.5, 434.5, 434.5, 459.53360559999999, 483.31192019999997, 504.64260099999996, 522.4560393999999, 535.85900099999992, 544.17939000000001, 547.0, 544.17939000000001, 535.85900099999992, 522.4560393999999, 504.64260099999996, 483.31192019999997, 459.53360559999999, 434.5, 434.5, 434.5, 434.5, 434.5, 410.36111069999998, 386.22222139999997, 362.08333589999995, 337.94444269999997, 313.80555699999996, 289.66667200000001, 265.52777099999997, 241.38888500000002, 217.25, 193.11111499999998, 168.972229, 144.83334399999998, 120.69445800000001, 96.555542000000003, 72.416656000000003, 48.277771000000001]
dSegZ = [24.138885000000002, 24.138886, 24.138885000000002, 24.138886, 24.13891600000001, 24.13888599999997, 24.138885000000016, 24.138885999999985, 24.138885000000016, 24.138885000000016, 24.138885999999957, 24.138901000000033, 24.13888499999996, 24.138885700000003, 24.138893199999984, 24.138885500000015, 24.138889300000017, 24.138889300000017, 0.0, 0.0, 0.0, 0.0, 25.033605599999987, 23.778314599999987, 21.330680799999982, 17.81343839999994, 13.402961600000026, 8.320389000000091, 2.820609999999988, 2.820609999999988, 8.320389000000091, 13.402961600000026, 17.81343839999994, 21.330680799999982, 23.778314599999987, 25.033605599999987, 0.0, 0.0, 0.0, 0.0, 24.138889300000017, 24.138889300000017, 24.138885500000015, 24.138893199999984, 24.138885700000003, 24.13888499999996, 24.138901000000033, 24.138885999999957, 24.138885000000016, 24.138885000000016, 24.138885999999985, 24.138885000000016, 24.13888599999997, 24.13891600000001, 24.138886, 24.138885000000002]
dBoomZ = [54.31, 54.31, 54.31, 54.31, 54.31, 54.31, 54.31, 79.51999999999998, 33, 33, 79.51999999999998, 54.31, 54.31, 54.31, 54.31, 54.31, 54.31, 54.31]

#-----------------------------------------------------------------------------------------------------
headers = list(df.columns.values)   #create list of all column (header) names
dataset = {}                        #create empty dictionary for all data

for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    dataset[header]=dfList      #Create dictionary item with header as its key and returns a list containing all datapoints

print
print "//"
steps = []      #indexes of the segments that mark the transition from one boom to another
dsteps = []     #the difference between the transition coordinates 

#Get a list with the indexes of the segments that lie partly in the first boom and partly in the next one
primerBoom = 0          #primer that runs through all the booms
primerSeg = 0           #primer that runs through all the segments
while primerBoom<len(BoomZ):
    if primerBoom < int(len(BoomZ)/2)+1:        #For the first half (that moves in positive Z): Check if the segment is further than the evaluated Boom.
        while BoomZ[primerBoom]>SegZ[primerSeg]:
            primerSeg = primerSeg + 1
    else:                                           #For the second half (that moves in negative Z): Check if the segment is further than the evaluated Boom.
        while BoomZ[primerBoom]<SegZ[primerSeg]:
            primerSeg = primerSeg + 1
    dsteps.append(abs(SegZ[primerSeg]-BoomZ[primerBoom]))       #Append the distance between segments steps
    steps.append(primerSeg)                                     #Append the index number of the segment step to steps list
    primerBoom = primerBoom + 1

#Set new lists to produe new datafiles
NewStress = []
NewUMag = []
NewU1 = []
NewU2 = []
NewU3 = []
NewX = []
NewY = []
NewZ = []


primerxlong = 0
while primerxlong < len(dataset['Index'])-1:  
    primerz = 0
    PrevSeg = 0

    #Define the reminders of the overlapping parts
    RemainStress = 0 
    RemainMag = 0
    RemainU1 = 0
    RemainU2 = 0
    RemainU3 = 0
    
    while primerz < len(steps):
        segments = range(PrevSeg,steps[primerz]+1,1)
        

        Stress = RemainStress
        Mag = RemainMag
        U1 = RemainU1
        U2 = RemainU2
        U3 = RemainU3
        
        factorsum = 0
        for segment in segments[:-1]:
            
            if primerz<18:            
                factor = float((dSegZ[segment])/float(dBoomZ[primerz])) #Percentage of the stress in the segment with respect to the lenght of the boom discretization length
                
            else:
                factor = float(24.138886/54.31)     #Manual override for program disability at last node ;)
            Stress = Stress + (dataset['MiseStress'][segment+primerxlong]*factor)
            Mag = Mag + (dataset['U.Mag'][segment+primerxlong]*factor)
            U1 = U1 + (dataset['U.U1'][segment+primerxlong]*factor)
            U2 = U2 + (dataset['U.U2'][segment+primerxlong]*factor)
            U3 = U3 + (dataset['U.U3'][segment+primerxlong]*factor)
            factorsum = factorsum + factor

        if primerz < 18:
            factor = 1-factorsum
            factor2 = ((dsteps[primerz])/dBoomZ[primerz])-factor #Percentage of the stress in the overlapping segment with respect to the lenght of the boom discretization length
            
            print factor
            print factor2
            
            Stress = Stress + (dataset['MiseStress'][segments[-1]+primerxlong])*factor
            RemainStress = (dataset['MiseStress'][segments[-1]+primerxlong])*(1-factor2)
            Mag = Mag + (dataset['U.Mag'][segments[-1]+primerxlong])*factor2
            RemainMag = (dataset['U.Mag'][segments[-1]+primerxlong])*(1-factor2)
            U1 = U1 + (dataset['U.U1'][segments[-1]+primerxlong])*factor2
            RemainU1 = (dataset['U.U1'][segments[-1]+primerxlong])*(1-factor2)
            U2 = U2 + (dataset['U.U2'][segments[-1]+primerxlong])*factor2
            RemainU2 = (dataset['U.U2'][segments[-1]+primerxlong])*(1-factor2)
            U3 = U3 + (dataset['U.U3'][segments[-1]+primerxlong])*factor2
            RemainU3 = (dataset['U.U3'][segments[-1]+primerxlong])*(1-factor2)
        
        NewX.append(dataset['x'][primerxlong])
        NewZ.append(BoomZ[primerz])
        NewY.append(BoomY[primerz])
        NewStress.append(Stress)
        NewUMag.append(Mag)
        NewU1.append(U1)
        NewU2.append(U2)
        NewU3.append(U3)
        
        PrevSeg = steps[primerz]+1
        primerz = primerz + 1
        
        break 

    primerxlong = primerxlong + 57

print
print '//Finished reordering'
#---------------------------------------------------------------------------------------------

#Put all data in a new empty dictionary
dataset = {}


dataset['x']= NewX
dataset['y']= NewY
dataset['z']= NewZ
dataset['MiseStress'] = NewStress
dataset['U.Mag'] = NewUMag
dataset['U.U1'] = NewU1
dataset['U.U2'] = NewU2
dataset['U.U3'] = NewU3



#Write new dataset to the csv file
newdf = pd.DataFrame(dataset)
newdf.to_csv(filenamOutput)

print
print '//Finished. Written data into:'
print filenamOutput



    
    
    
    
    
    
    
    