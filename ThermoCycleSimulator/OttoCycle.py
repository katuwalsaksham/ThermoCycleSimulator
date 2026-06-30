import matplotlib.pyplot as plt
import numpy as np
# This code is for otto cycle calculation
# Reference values are given for each input parameters in brackets
# State 1 is the starting point, the piston rests at bottom before compression
T1 = float(input("Enter initial temperature in Kelvin (280-300K): "))
P1 = float(input("Enter initial Pressure in Pascal (95,000-101,325 Pa): "))
r_k = float(input("Enter compression ratio (V1/V2) (8-12): "))
gamma = float(input("Enter ratio of specefic heats,gamma (Cp/Cv) (1.4 for air): "))
Q_in = float(input("Enter heat added in J/Kg, Q_in (800,000-1500,000 J/Kg): "))
Cv = float(input("Enter the value of sepcefic heat at constant valume in J/Kg*K (718 J/Kg*k for air): "))
R = 287 #USpecefic gas constant for air :J/Kg*k
m = 1 #per kg of air
V1 = (m*R*T1)/P1
S1 = 0 #reference
# isentropic compression(Stage 1-2), piston is at top (State 2)
T2 = T1 * (r_k ** (gamma - 1))
P2 = P1 * (r_k**gamma)
V2 = (m*R*T2)/P2
S2 = S1 #Isentropic process

# isochoric heat addition(Stage 2-3), fuel is just burnt,Piston at TDC (State 3)
T3 = T2 + (Q_in / Cv)
P3 = P2 * (T3 / T2)
V3 = V2
S3 = S2  + Cv* (np.log(T3/T2))  # Isochoric process: change in entropy = Cv *ln(T_final/T_initial)

# isentropic expansion(Stage 3-4), piston at BDC (State 4)
T4 = T3 / (r_k ** (gamma - 1))
P4 = P3 / (r_k**gamma)
V4 = (m*R*T4)/P4
S4 = S3
Efficiency = (1-(1/(r_k**(gamma-1))))*100
# isochoric heat rejection(Stage 4-1)
V12 = np.linspace(V1,V2,100) #100 equally spaced points between V1 and V2
V23 = np.array([V2,V3]) # Constant volume same vertical line
V34 = np.linspace(V3,V4,100) 
V41 = np.array([V4,V1]) 

P12 = P1* (V1**gamma) /(V12**gamma) #PV**gamma = constant
P23 = np.array([P2,P3]) 
P34 = P3* (V3**gamma) /(V34**gamma) 
P41 = np.array([P4,P1]) 

S12 = np.array([S1,S2])
S23 = np.linspace(S2,S3, 100)
S34 = np.array([S3,S4])
S41 = np.linspace(S4,S1, 100)

T12 = np.array([T1,T2]) 
T23 = T2 * np.exp((S23 - S2)/Cv)
T34 = np.array([T3,T4]) 
T41 = T4 * np.exp((S41 - S4)/Cv)
# Printing Values of temperature at different stages
print(f"Initial temperature T1= {T1:.2f} K")
print(f"After isentropic compression T2= {T2:.2f} K")
print(f"After isochoric heat addition T3= {T3:.2f} K")
print(f"After isentropic expansion T4= {T4:.2f} K")

# Printing Values of pressure at different stages
print(f"Initial Pressure P1= {P1:.2f} Pa")
print(f"After isentropic compression P2= {P2:.2f} Pa")
print(f"After isochoric heat addition P3= {P3:.2f} Pa")
print(f"After isentropic expansion P4= {P4:.2f} Pa")
print(f"The efficiency of the cycle = {Efficiency:.2f}")

#plotting the PV diagram
plt.figure(figsize=(10,8))
plt.plot(V12,P12, color ='b',linestyle = '--', label = '1->2 Isentropic Compression')
plt.plot(V23,P23, color ='g',linestyle = '--', label = '2->3 Isochoric Heat Addition')
plt.plot(V34,P34, color ='r',linestyle = '--', label = '3->4 Isentropic Expansion')
plt.plot(V41,P41, color ='m',linestyle = '--', label = '4->1 Isochoric Heat Rejection')
plt.title("Otto cycle PV diagram", color = 'r')
plt.xlabel('Volume(m^3/kg)')
plt.ylabel('Pressure(Pa)')
plt.grid(True , linestyle = '--')
# plt.legend()
# plt.show()

#Plotting the TS diagram
plt.figure(figsize=(10,8))
plt.plot(S12,T12, color ='b',linestyle = '--', label = '1->2 Isentropic Compression')
plt.plot(S23,T23, color ='g',linestyle = '--', label = '2->3 Isochoric Heat Addition')
plt.plot(S34,T34, color ='r',linestyle = '--', label = '3->4 Isentropic Expansion')
plt.plot(S41,T41, color ='m',linestyle = '--', label = '4->1 Isochoric Heat Rejection')
plt.title("Otto cycle TS diagram", color = 'r')
plt.xlabel('Entropy(J/K)')
plt.ylabel('Temperature(K)')
plt.grid(True , linestyle = '--')
plt.legend()
plt.show()