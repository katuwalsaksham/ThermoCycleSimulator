import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI

# This code calculates different parameters for rankine cycle and plots The PV and TS diagram
Fluid = "Water"  # Working Fluid
P_Condender = float(input("Enter condenser pressure in Pascal (5,000-15,000 Pa): "))
P_Boiler = float(input("Enter boiler pressure in Pascal (5,000,000-15,000,000 Pa): "))

# Saturated liquid leaving the Condener, state 1
P1 = P_Condender
T1 = PropsSI("T", "P", P1, "Q", 0, Fluid)
H1 = PropsSI("H", "P", P1, "Q", 0, Fluid)
S1 = PropsSI("S", "P", P1, "Q", 0, Fluid)
V1 = 1 / PropsSI("D", "P", P1, "Q", 0, Fluid)  # Speccefic Volume

# isentropic compression(Stage 1-2), State 2, compressed(subcooles) liquid leaving the pump
P2 = P_Boiler
S2 = S1
T2 = PropsSI("T", "P", P2, "S", S2, Fluid)
H2 = PropsSI("H", "P", P2, "S", S2, Fluid)
V2 = 1 / PropsSI("D", "P", P2, "S", S2, Fluid)
W_pump = H2 - H1  # Work done by pump per unit kg mass
# isobaric head addition(Stage 2-3), State 3, satueated vapour leaving the boiler
P3 = P2
T3 = PropsSI("T", "P", P3, "Q", 1, Fluid)
H3 = PropsSI("H", "P", P3, "Q", 1, Fluid)
S3 = PropsSI("S", "P", P3, "Q", 1, Fluid)
V3 = 1 / PropsSI("D", "P", P3, "Q", 1, Fluid)
Q_in = H3 - H2  # heat added to boiler per unit kg mass

# isentropic expansion(Stage 3-4), State 4, Wet steam entering condenser
P4 = P_Condender
S4 = S3
T4 = PropsSI("T", "P", P4, "S", S4, Fluid)
H4 = PropsSI("H", "P", P4, "S", S4, Fluid)
V4 = 1 / PropsSI("D", "P", P4, "S", S4, Fluid)
W_turbine = H3 - H4

# isobaric heat rejection(Stage 4-1)
Q_out = H4 - H1

W_net = W_turbine - W_pump
Efficiency = (W_net / Q_in) * 100
Efficiency_check = (1 - (Q_out / Q_in)) * 100

print(f"Initial Pressure P1= {P1:.2f} Pa")
print(f"After isentropic compression P2= {P2:.2f} Pa")
print(f"After isobaric heat addition P3= {P3:.2f} Pa")
print(f"After isentropic expansion P4= {P4:.2f} Pa")

print(f"Initial Temperature T1= {T1:.2f} K")
print(f"After isentropic compression T2= {T2:.2f} K")
print(f"After isobaric heat addition T3= {T3:.2f} K")
print(f"After isentropic expansion T4= {T4:.2f} K")

print(f"The efficiency of the cycle = {Efficiency:.2f}%")
print(f"Checking the efficiency = {Efficiency_check:.2f}%")

print(f"Pump work    = {W_pump/1000:.2f} kJ/kg")
print(f"Turbine work = {W_turbine/1000:.2f} kJ/kg")
print(f"Heat added   = {Q_in/1000:.2f} kJ/kg")


# Plotting the PV diagram
P12 = np.linspace(P1, P2, 100)
V12 = np.array([1 / PropsSI("D", "P", p, "S", S1, Fluid) for p in P12])

V23 = np.array([V2, V3])
P23 = np.array([P2, P3])

P34 = np.linspace(P3, P4, 100)
V34 = np.array([1 / PropsSI("D", "P", p, "S", S3, Fluid) for p in P34])

V41 = np.array([V4, V1])
P41 = np.array([P4, P1])

plt.figure(figsize=(10, 8))
plt.plot(V12, P12, color="b", linestyle="--", label="1->2 Isentropic Compression")
plt.plot(V23, P23, color="g", linestyle="--", label="2->3 Isobaric Heat Addition")
plt.plot(V34, P34, color="r", linestyle="--", label="3->4 Isentropic Expansion")
plt.plot(V41, P41, color="m", linestyle="--", label="4->1 Isobaric Heat Rejection")
plt.title("Rankine cycle PV diagram", color="r")
plt.xlabel("Volume(m^3/kg)")
plt.ylabel("Pressure(Pa)")
plt.grid(True, linestyle="--")
points_V = [V1, V2, V3, V4]
points_P = [P1, P2, P3, P4]
labels = ["1", "2", "3", "4"]
plt.scatter(points_V, points_P, color="k", zorder=5)
for x, y, label in zip(points_V, points_P, labels):
    plt.annotate(
        label,
        (x, y),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=10,
        fontweight="normal",
    )

plt.legend()

# Plotting the TS diagram
S12 = np.array([S1, S2])
T12 = np.array([T1, T2])

# S3_sat_liquid = PropsSI("S", "P", P3, "Q", 0, Fluid)

# S23_preheat = np.array([S2, S3_sat_liquid])
# T23_preheat = np.array([T2, T3])

# S23_boil = np.array([S3_sat_liquid, S3])
# T23_boil = np.array([T3, T3])

# S23 = np.concatenate([S23_preheat, S23_boil])
# T23 = np.concatenate([T23_preheat, T23_boil])
H23 = np.linspace(H2, H3, 100)
S23 = np.array([PropsSI("S", "P", P3, "H", h, Fluid) for h in H23])
T23 = np.array([PropsSI("T", "P", P3, "H", h, Fluid) for h in H23])


S34 = np.array([S3, S4])
T34 = np.array([T3, T4])

S41 = np.array([S4, S1])
T41 = np.array([T4, T1])


plt.figure(figsize=(10, 8))
plt.plot(S12, T12, color="b", linestyle="--", label="1->2 Isentropic Compression")
plt.plot(S23, T23, color="g", linestyle="--", label="2->3 Isobaric Heat Addition")
plt.plot(S34, T34, color="r", linestyle="--", label="3->4 Isentropic Expansion")
plt.plot(S41, T41, color="m", linestyle="--", label="4->1 Isobaric Heat Rejection")
plt.title("Rankine cycle TS diagram", color="r")
plt.xlabel("Entropy(J/K)")
plt.ylabel("Temperature(K)")
plt.grid(True, linestyle="--")
points_S = [S1, S2, S3, S4]
points_T = [T1, T2, T3, T4]
labels = ["1", "2", "3", "4"]
plt.scatter(points_S, points_T, color="k", zorder=4)
for x, y, label in zip(points_S, points_T, labels):
    plt.annotate(label, (x, y), xytext=(8, 8), textcoords="offset points", fontsize=10)
plt.legend()
plt.show()
