import numpy as np
import matplotlib.pyplot as plt

def CurrentTransferRatio  (VoltageIn, VoltageOut, Resistance):
   CurrentIn = np.zeros(len(VoltageOut))
   CurrentOut = np.zeros(len(VoltageOut))
   CTR = np.zeros(len(VoltageOut))
   for i in range (0,len(VoltageOut)):
        CurrentIn[i] = (VoltageIn[i] * 10**-3) / Resistance # A Through R1
        CurrentOut[i] = (VoltageOut[i] * 10**-3) / Resistance # A Through R2
        CTR[i] = (CurrentOut[i] / CurrentIn[i]) * 100 # CTR %
        
   return CurrentIn, CurrentOut, CTR 

Res = 110 #Ohm for R1 and R2 

#Batch #2038 MEX -1st Opto
VoltageIn =     [.3, 0.8, 2,    4.9, 11.7, 25.4, 47.8, 77.7,  112.4, 149.9,  189.7, 230, 271.5, 314.5] #mV Across R1
VoltageOut =    [0,  0,   0.1,  0.9, 5.1,  20.9, 58.8, 122.4, 205.4,  300.4, 406.3, 506, 570.3, 609.4] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#2038 MEX -1')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#2038 MEX -1')

#Batch #2038 MEX -2nd
VoltageIn =     [0.3, 0.8, 2.2, 5.2, 12.4, 26.6,  49.3, 79.5,  114.1,  151.5, 190.8, 231.5, 273.5, 317] #mV Across R1
VoltageOut =    [0,     0, 0,   0.2,  2.4,  13.5, 45.5, 105.8, 190.5,   294,  412.5,   538.5,   657.3, 728] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#2038 MEX -2')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#2038 MEX -2 ')

#Batch #2038 MEX -3rd
VoltageIn =     [0.4, 1.1, 2.8, 7,   16.4, 33.9, 59.8, 92.3,  128.3,  166.5, 208.8, 247.9, 289.6, 333] #mV Across R1
VoltageOut =    [0,     0, 0,   0.6, 5.7,  26.4, 74.3, 151.4, 249.1,  361.8, 485.5, 610.0, 697,   748] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#2038 MEX -3')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#2038 MEX -3 ')

#Batch #0514 MEX -1st
VoltageIn =     [3.9, 9.5, 20.8, 39.7, 66.5,  98.7, 134.9, 174.4,  215.1,  257.1,  300.3, 344, 388.2, 433.5] #mV Across R1
VoltageOut =    [0.2, 1.2, 3.4,  9.5,  42.7,  80.2, 128,   184.4,   231.3,  280.3,  310.3, 334.1, 354.6, 361.2] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#0514 MEX -1')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#0514 MEX -1')

#Batch #0514 MEX -2nd
VoltageIn =     [3.9, 9.3, 20.6, 39.6, 66.3,  98.4,  134.5, 173.9,  214.7,  256.5,  299.6, 343, 387.2, 432.4] #mV Across R1
VoltageOut =    [0.3, 1.5, 7.2,  23.6,  56.5, 105.6, 168.5,   240.5,   294,  329.4,  356.8, 379.5, 399.5, 417.8] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#0514 MEX -2')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#0514 MEX -2')

#Batch #1022 MEX -1st
VoltageIn =     [.5, 1.4, 3.7, 9.1, 20.6,  40.3, 68.1, 102.1,  139.9,  179.3,  221.1, 263.7, 307.1, 351.2] #mV Across R1
VoltageOut =    [0,  0,   0.1,  0.6,  3.1,  10.5, 28,   54.4,   88.3,  127.6,  171.3, 219.4, 269.2, 322] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#1022 MEX -1')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#1022 MEX -1')

#Batch #1022 MEX -2nd
VoltageIn =     [1, 2.5, 6.2, 14.3, 29.5,  52.7, 82.7, 118.2,  156.5,  196.7,  238.9, 281.5, 325.3, 370.3] #mV Across R1
VoltageOut =    [0,   0, 0.1,  0.8,  3.5,  11,  24.8,   45.4,   69.4,  101.2,  134.8, 170.5, 208.5, 248] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#1022 MEX -2')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#1022 MEX -2')

#Batch #1022 MEX -3rd
VoltageIn =     [0.7, 1.8, 4.6, 11.1, 24.1,  45.4, 74.2, 108.9,  146.7,  186.7,  228.5, 271.1, 314.6, 359.5] #mV Across R1
VoltageOut =    [0,   0,   0.2,  1.0,  4.9,  16.3,  38.2, 71.1,   111.8,  158.9, 211.1, 266.3, 324.3, 384.8] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#1022 MEX -3')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#1022 MEX -3')

#Batch #0916 MEX -1st
VoltageIn =     [0.6, 1.6, 4.1, 10.1, 22.1, 41.5, 69,   102.5, 139.9, 179.2, 221,   263,   306.1, 350.5] #mV Across R1
VoltageOut =    [0,   0,   0.1, 0.6,  3.1,  11.2, 28.6, 62,    95.2,  139.2, 191.3, 246.3, 302.5, 364] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#0916 MEX -1')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#0916 MEX -1')

#Batch #2245 MEX -1st
VoltageIn =     [0.3, 0.8, 2.1, 5.2, 12.5, 26.7, 49.3,  79.3, 113.6, 150.8, 190.3, 230.6, 272.3, 315.2] #mV Across R1
VoltageOut =    [0,   0,   0.1, 0.5,  2.8,  11.1, 30.6, 63.5, 106.7,  157.6, 215,  275.9, 340.0, 407.5] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#2245 MEX -1')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#02245 MEX -1')

#Batch #2245 MEX -2nd
VoltageIn =     [0.3, 0.8, 2.1, 5.2, 12.2, 26.3,  48.6,  78.4, 112.5, 149.6, 189.1, 229.5, 271.3, 313.9] #mV Across R1
VoltageOut =    [0,   0,   0.1, 0.5,  2.8,  11.4, 32.3, 67.9,  115.3, 171.4, 234.9, 302.2, 373.5, 448.4] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#2245 MEX -2')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#02245 MEX -2')

#Batch #2245 MEX -3rd
VoltageIn =     [0.3, 0.7, 1.9, 4.7, 11.3, 24.6,  46.2, 75.4, 109.2, 145.9, 184.9, 225.1, 266.3, 309.9] #mV Across R1
VoltageOut =    [0,   0,   0,   0.4,  2.5,  10.4, 29.6, 63.0, 107.6, 160.5, 220.4, 284.2, 351.1, 422.3] #mV Across R2
CurrentIn, CurrentOut, CTR  = CurrentTransferRatio  (VoltageIn, VoltageOut, Res)
plt.figure(1)
plt.plot(CurrentOut*10**3, CTR, label='#2245 MEX -3')
plt.figure(2)
plt.plot(CurrentOut*10**3, CurrentIn*10**3, label='#2245 MEX -3')


plt.figure(1)
plt.legend()
plt.xlabel('Current Output (mA)(Vout = 1.1, V R2 = 110 Ω)')
plt.ylabel('CTR(%)')
plt.title('OP110C CTR Batch Comparison')
plt.figure(2)
plt.legend()
plt.xlabel('Current Output (mA) (Vout = 1.1, V R2 = 110 Ω)')
plt.ylabel('Current Input (mA) (Vin 0.9 V to 1.55 V, R1 = 110 Ω)')
plt.title('OP110C Batch Current Out vs Current In Comparison')

plt.show()