def Colour2Temp (RGB, MaxTemp, MinTemp): 
    import numpy as np 
    min =  np.array([24, 24, 24])
    low  = np.array([150, 31, 159])
    lowMid = np.array([189, 74, 87])
    mid = np.array([244, 136, 2])
    highMid = np.array([244, 186, 7])
    high = np.array([244, 210, 60])
    veryHigh = np.array([244, 217, 137])
    Max = np.array([255, 255, 255])
    tempTemp = RangeOut(MinTemp, MaxTemp)
    if np.all(RGB < min): temp = MinTemp
    elif np.all(RGB < low): temp = .14*tempTemp+MinTemp
    elif np.all(RGB < lowMid): temp = .28*tempTemp+MinTemp
    elif np.all(RGB < mid): temp = .42*tempTemp+MinTemp
    elif np.all(RGB < highMid): temp = .56*tempTemp+MinTemp
    elif np.all(RGB < high): temp = .70*tempTemp+MinTemp
    elif np.all(RGB < veryHigh): temp = .84*tempTemp+MinTemp
    elif np.all(RGB < Max): temp = .95*tempTemp+MinTemp
    else: temp = MaxTemp
    return temp

def RangeOut(Xmin, Xmax):
    return (Xmax-Xmin)

RGB = 209,105,42
print(Colour2Temp(RGB, 46,23))
