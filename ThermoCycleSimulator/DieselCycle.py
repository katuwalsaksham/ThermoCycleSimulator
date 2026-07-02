import matplotlib.pyplot as plt
import numpy as np

# This code calculates different parameters of Diesel Cycle and plots the PV and TS diagram
# Reference values are given for each input parameters in brackets
T1 = float(input("Enter initial temperature in Kelvin (280-300K): "))
P1 = float(input("Enter initial Pressure in Pascal (95,000-101,325 Pa): "))
r_k = float(input("Enter compression ratio (V1/V2) (16-20): "))
gamma = float(input("Enter ratio of specefic heats,gamma (Cp/Cv) (1.4 for air): "))
Q_in = float(input("Enter heat added in J/Kg, Q_in (800,000-1500,000 J/Kg): "))
Cv = float(
    input(
        "Enter the value of sepcefic heat at constant valume in J/Kg*K (718 J/Kg*k for air): "
    )
)
Cp = float(
    input(
        "Enter the value of sepcefic heat at constant pressure in J/Kg*K (1005 J/Kg*k for air): "
    )
)
R = 287  # USpecefic gas constant for air :J/Kg*k
m = 1  # per kg of air
V1 = (m * R * T1) / P1
S1 = 0  # reference
# isentropic compression(Stage 1-2), State 2
T2 = T1 * (r_k ** (gamma - 1))
P2 = P1 * (r_k**gamma)
V2 = V1 / r_k
S2 = S1  # Isentropic process

# isobaric heat injection(Stage 2-3),State 3
T3 = T2 + (Q_in / Cp)
P3 = P2  # isobaric process
V3 = V2 * (T3 / T2)
S3 = S2 + Cp * (np.log(T3 / T2))

# isentropic expansion(Stage 3-4), State 4
r_c = V3 / V2  # cutoff ratio - how much volume is expanded during fuel injection
r_e = r_k / r_c
T4 = T3 / (r_e ** (gamma - 1))
P4 = P3 / (r_e**gamma)
V4 = (m * R * T4) / P4
S4 = S3
# isochoric heat rejection(Stage 4-1) V4 = V1
num = ((r_c) ** gamma) - 1
den = gamma * (r_c - 1)
Efficiency = (1 - ((1 / ((r_k) ** (gamma - 1))) * (num / den))) * 100

# Checking the efficiency
Q_out = Cv * (T4 - T1)
Efficiency_check = (1 - (Q_out / Q_in)) * 100

# Printing Values of pressure at different stages
print(f"Initial Pressure P1= {P1:.2f} Pa")
print(f"After isentropic compression P2= {P2:.2f} Pa")
print(f"After isobaric heat addition P3= {P3:.2f} Pa")
print(f"After isentropic expansion P4= {P4:.2f} Pa")
print(f"The efficiency of the cycle = {Efficiency:.2f}")
print(f"Checking the efficiency = {Efficiency_check:.2f}")

# Plotting the PV diagram
V12 = np.linspace(V1, V2, 100)  # 100 equally spaced points between V1 and V2
P12 = P1 * (V1**gamma) / (V12**gamma)  # PV**gamma = constant

V23 = np.array([V2, V3])
P23 = np.array([P2, P3])  # Constant Pressure

V34 = np.linspace(V3, V4, 100)
P34 = P3 * (V3**gamma) / (V34**gamma)

V41 = np.array([V4, V1])
P41 = np.array([P4, P1])

plt.figure(figsize=(10, 8))
plt.plot(V12, P12, color="b", linestyle="--", label="1->2 Isentropic Compression")
plt.plot(V23, P23, color="g", linestyle="--", label="2->3 Isobaric Heat Addition")
plt.plot(V34, P34, color="r", linestyle="--", label="3->4 Isentropic Expansion")
plt.plot(V41, P41, color="m", linestyle="--", label="4->1 Isochoric Heat Rejection")
plt.title("Diesel cycle PV diagram", color="r")
plt.xlabel("Volume(m^3/kg)")
plt.ylabel("Pressure(Pa)")
plt.grid(True, linestyle="--")
points_V = [V1,V2,V3,V4]
points_P = [P1,P2,P3,P4]
labels = ['1','2','3','4']
plt.scatter(points_V,points_P, color = 'k' , zorder =5)
for x,y,label in zip(points_V,points_P,labels):
    plt.annotate(label,(x,y), xytext=(5,5),textcoords="offset points",fontsize = 10,fontweight = 'normal')

plt.legend()
# plt.show()

# Plotting the TS diagram
S12 = np.array([S1, S2])
T12 = np.array([T1, T2])

S23 = np.linspace(S2, S3, 100)
T23 = T2 * np.exp((S23 - S2) / Cp)

S34 = np.array([S3, S4])
T34 = np.array([T3, T4])

S41 = np.linspace(S4, S1, 100)
T41 = T4 * np.exp((S41 - S4) / Cv)

plt.figure(figsize=(10, 8))
plt.plot(S12, T12, color="b", linestyle="--", label="1->2 Isentropic Compression")
plt.plot(S23, T23, color="g", linestyle="--", label="2->3 Isobaric Heat Addition")
plt.plot(S34, T34, color="r", linestyle="--", label="3->4 Isentropic Expansion")
plt.plot(S41, T41, color="m", linestyle="--", label="4->1 Isochoric Heat Rejection")
plt.title("Diesel cycle TS diagram", color="r")
plt.xlabel("Entropy(J/K)")
plt.ylabel("Temperature(K)")
plt.grid(True, linestyle="--")
points_S = [S1,S2,S3,S4]
points_T = [T1,T2,T3,T4]
labels = ['1','2','3','4']
plt.scatter(points_S,points_T, color ='k',zorder = 4)
for x,y,label in zip(points_S,points_T,labels):
    plt.annotate(label,(x,y), xytext = (8,8), textcoords='offset points',fontsize = 10)
plt.legend()
plt.show()
