import numpy as np
Ca      =   0.547       #[m]
la      =   2.771       #[m]
x1      =   0.153       #[m]
x2      =   1.281       #[m]
x3      =   2.681       #[m]
xa      =   0.28        #[m]
h       =   0.225       #[m]
tsk     =   1.1*10**-3   #[m]     
tsp     =   2.9*10**-3   #[m]
tst     =   1.2*10**-3   #[m]
hst     =   1.5*10**-2   #[m]
wst     =   2.0*10**-2   #[m]
nst     =   17
d1      =   1.103*10**-2 #[m]
d3      =   1.642*10**-2 #[m]
theta   =   26          #[deg]
P       =   91700       #[N]
q       =   4530        #[N/m]
Iyy     =   261143990,8*10**-12     #[m^4]
Izz     =   11991695,56*10**-12     #[m^4]

radius = h/2                #[m]
tribase =   Ca-radius       #[m], length of triangle base 


#Produce mock locations for intermediate usage
xmock = la/2
ymock = 0
zmock = Ca/2

print xmock,ymock,zmock

#END OF MOCK RESULTS

Sy = 1

S12 = radius                            #length of segment 12
S23 = np.sqrt(radius**2+tribase**2)     #length of segment 23

qb23 = -Sy/Izz*(radius/(2*S23))*s1**2           #basic shearflow calculation segment 23
qb12 = -(Sy/Izz*(radius)*s2)-(Sy/Izz*(radius/(2*S23))*S23**2) #basic shearflow calculation segment 12









