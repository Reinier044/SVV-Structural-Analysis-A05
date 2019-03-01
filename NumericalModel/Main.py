import numpy as np
import matplotlib.pyplot as plt
from reactions_v_26Feb import torsion, VZ, VY, ydeflection,Mz
import pandas as pd

# Variables
sections = 113

# Geometric constants
la = 2771.  # mm
t1 = 1.1  # mm (skin thickness)
t2 = 2.9  # mm (spar thickness)
Ca = 547.  # mm
h = 225.  # mm
G = 28000.  # N/mm^2

# Calculation constants
r = h/2
A1 = (r) ** 2 * np.pi / 2
A2 = (Ca - r) * r
s1 = np.pi * r  # nose part total circumference
s2 = 2 * np.sqrt(r ** 2 + (Ca - r) ** 2)  # triangle part total circumference
dstr = (s1 + s2) / 17
tht2 = dstr / r
tht3 = tht2
tht1 = np.pi / 2 - tht2
tht4 = tht1
phi = np.tan(r / (Ca - r))
p_tr = np.sin(np.pi / 2 - phi) * r

#
Vz = VZ  # import
Vy = VY
var = 0
T = np.zeros(sections)
for j in range(sections):
    T[j] = torsion(var)
    var += la / sections
Mo = np.zeros(sections)
for j in range(sections):
    Mo[j] = torsion(var)

#Geometrical properties
Iyy = 52013464.25  # mm^4
Izz = 11996389.06  # mm^4
Area = np.array(
    [0, 103.71, 103.71, 103.71, 103.71, 103.71, 103.71, 103.71, 182.19, 129.75, 106.83, 129.75, 182.19, 103.71, 103.71,
     103.71, 103.71, 103.71, 103.71, 103.71])
zloc = np.array(
    [0, 54.31, 108.62, 162.93, 217.24, 271.55, 325.86, 380.17, 434.48, 514, 547, 514, 434.48, 380.17, 325.86, 271.55,
     217.24, 162.93, 108.62, 54.31])
zloc = zloc - 304.93
yloc = np.array(
    [0., -14.0625, -28.125, -42.1875, -56.25, -70.3125, -84.375, -98.4375, -112.5, -79.55, 0., 79.55, 112.5, 98.4375,
     84.375, 70.3125, 56.25, 42.1875, 28.125, 14.0625])

# Empty arrays
twist = np.zeros(sections)
qby = np.zeros(sections)
qbz = np.zeros(sections)
qb = np.zeros([20, sections])
q_shear_bend = np.zeros([20, sections])
delta_qb = np.zeros([20, sections])  # index 1 for boom 1 etc. Note: index 0 represents a nonexistent boom and is not used!
qs01 = np.zeros(sections)
qs02 = np.zeros(sections)
qsum1 = np.zeros(sections)
qsum2 = np.zeros(sections)
Vali_stress = np.zeros(sections)
VM_stresses = np.zeros([20,sections])

# Shear flows and twist due to Torque (x-axis)
for i in range(0, sections):
    eqn = np.array([[2 * A1, 2 * A2, 0], [(s1 / t1 + h / t2) / (2 * A1 * G), -h / (2 * A1 * G * t2), -1],
                    [-h / (2 * A2 * G * t2), (s2 / t1 + h / t2) / (2 * A2 * G), -1]])
    sol = np.array([[T[i]], [0], [0]])
    x = np.linalg.solve(eqn, sol)
    twist[i] = x[2]*la/sections+twist[i-1]
    qs01[i] = x[0]
    qs02[i] = x[1]

# Calculation of 'open section' shear flows
for i in range(0, sections):
    qby[i] = -Vz[i] / Iyy
    qbz[i] = -Vy[i] / Izz
    qb[11][i] = 0.
    qb[12][i] = 0.

    for j in range(1, 20):
        delta_qb[j][i] = qby[i] * Area[j] * zloc[j] + qbz[i] * Area[j] * yloc[
            j]  # jump in 'open section' shear flow at boom j
    qb[10][i] = 0 + delta_qb[11][i]  # These 4 lines are for cell 1
    qb[9][i] = qb[10][i] + delta_qb[10][i]
    qb[8][i] = qb[9][i] + delta_qb[9][i]

    qb_0_II = 0 + delta_qb[12][i]  # Positive downward
    qb[0][i] = -qb_0_II  # Positive downward

    qb[7][i] = qb_0_II + delta_qb[8][i]
    for j in range(6, 0, -1):
        qb[j][i] = qb[j + 1][i] + delta_qb[j + 1][i]

    qb[19][i] = qb[1][i] + delta_qb[1][i]
    for j in range(18, 12, -1):
        qb[j][i] = qb[j + 1][i] + delta_qb[j + 1][i]
    for j in range(8, 12):
        qsum1[i] += (qb[j][i] * dstr) / t1
    for j in range(1, 8):
        qsum2[i] += 2 * (qb[j][i] * dstr) / t1
    for j in range(12, 20):
        qsum2[i] += 2 * (qb[j][i] * dstr) / t1

# Deflection due to shear
for i in range(0, sections):
    Mo_nose_qb = qb[11][i] * r ** 2 * tht1 + qb[10][i] * r ** 2 * tht2 + qb[9][i] * r ** 2 * tht3 \
                 + qb[8][i] * r ** 2 * tht4
    dummy = 0
    for j in [6, 5, 4, 3, 2, 1, 19, 18, 17, 16, 15, 14, 13]:
        dummy = dummy + qb[j][i] *p_tr* dstr
    Mo_triangle_qb = qb[7][i] * p_tr * ((s2 - 13 * dstr) / 2) + dummy

    eqn = np.array([[2 * A1, 2 * A2, 0], [(s1 / t1 + h / t2) / (2 * A1), -h / (2 * A1 * t2), -1],
                    [-h / (2 * A2 * t2), (h / t2 + s1 / t1) / (2 * A2), -1]])
    sol = np.array([[-Mo_nose_qb - Mo_triangle_qb + Mo[i]], [(-qsum1[i] - qb[0][i] * h / t2) / (2 * A1 * G)],
                    [(-qsum2[i] - qb[0][i] * h / t2) / (2 * A1 * G)]])
    x2 = np.linalg.solve(eqn, sol)
    twist[i] += x2[2]*la/sections+twist[i - 1]

    for j in range(1, 8):
        q_shear_bend[j][i] = qb[j][i] + x2[1] + qs02[i]
    for j in range(12, 20):
        q_shear_bend[j][i] = qb[j][i] + x2[1] + qs02[i]
    for j in range(8, 12):
        q_shear_bend[j][i] = qb[j][i] + x2[0] + qs01[i]
    q_shear_bend[0][i] = qb[0][i] + x2[0] - x2[1] + qs01[i]  # positive upward


##Deflection total
Ley = np.zeros(sections)
Tey = np.zeros(sections)
for i in range(0,sections):
   Ley[i] = -np.sin(twist[i])*r-ydeflection[i]
   Tey[i] = np.sin(twist[i])*(Ca-r)-ydeflection[i]

#Von Mises stresses
for i in range(sections):
    for j in range(20):
        VM_stresses[j,i] = abs(q_shear_bend[j,i]/dstr)+Mz[i]*yloc[j]/Izz

#VM stress from Reinier
name = "LC1"
filenameInput = 'A320_Comp_'+name+'.csv'

df = pd.read_csv(filenameInput)
print()
print ("//Imported data")

headers = list(df.columns.values)
dataset = {}

flag = 0
for header in headers:
    dfToList = df[header].tolist()
    dfList = list(df[header])
    if flag>0:
        dataset[header]=dfList
    flag = flag + 1

for i in range(sections):
    Vali_stress[i] = dataset["MiseStress"][9+19*i]
    if dataset["MiseStress"][9+19*i] == 0.0 :
        Vali_stress[i] = Vali_stress[i-1]

# Plotting shear flows
im = plt.imread("Figure2.png")
implot = plt.imshow(im)
y = [265, 340, 350, 360, 370, 380, 390, 390, 380, 310, 230, 160, 140, 140, 150, 160, 170, 180, 190, 200]
z = [210, 570, 510, 450, 390, 330, 270, 210, 150, 100, 90, 130, 190, 250, 310, 370, 430, 490, 550, 650]
for i in range(20):
    plt.annotate(round(q_shear_bend[i, 56],2), (z[i], y[i]))  # adjust to choose slice
plt.xlabel("z")
plt.ylabel("y")
plt.title("Shear flows")
plt.show()

#Plotting Von Mises Stresses
plt.title("Von Mises stresses")
plt.ylabel('$\sigma$[MPa]')
plt.xlabel("span")
plt.plot(VM_stresses[9], label = "Numerical")
plt.plot(Vali_stress,label = 'Finite Element')
plt.legend()
plt.show()

#Plotting Twist
plt.title("twist")
plt.ylabel("angle")
plt.xlabel("sections")
plt.plot(twist)
plt.show()
