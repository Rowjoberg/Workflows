import numpy as np

# Current Divider 
# R1 = 470e3 #Ohms
# R2 = 1e3 #Ohms
# R3 = 60e3 #Ohms
# R4 = 20e3 #Ohms
# V1 = 30 #Volts
# Zeq = ((R1)**-1+ (R2+ R3 +R4)**-1)**-1
# print("Zeq = ", Zeq)
# Ieq = V1 / Zeq
# print("Ieq = ", Ieq)
# I2 = V1 / R1
# print("I2 = ", I2)
# I1 = Ieq * (R1 / (R1 + R2 + R3 +R4))
# print("I1 = ", I1)
# print("Check Ieq = ", I1 +I2)
# V2 = V1 - (I1 * R2)
# print("V2 = ",V2)
# V3 = V2 - (I1 * R3)
# print("V3 = ",V3)

# Voltage Divider 
# R1 = 470e3 #Ohms
# R2 = 1e3 #Ohms
# V1 = 30 #Volts
# V2 = V1 * ((R2) / (R2+R1))
# print("V2 = ",V1-V2)


# 3 Phase to single Phase
# Vline = 3300
# Vphase = Vline / np.sqrt(3)
# print(Vphase)

# Single Phase to 3 Phase
# VPhase = 1000
# Vline = VPhase * np.sqrt(3)
# print(Vline)

# RMS Voltage
# Vpeak = 60
# print(Vpeak/np.sqrt(2))

Z = 390*(270/390)
print(Z)
I = 3 / 390
V = 3-I*120
print(3-I*120)