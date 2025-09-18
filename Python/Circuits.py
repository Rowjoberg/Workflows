def parallel(Resistances):
    """
    Parallel Example
    from Circuits import parallel
    R1, R2, R3 = 100, 100, 100
    print(parallel([R1, R2, R3]))
    """
    y = 0
    for i in range(0, len(Resistances)):
        y = Resistances[i] ** -1 + y
    return y**-1


def NormalisedImpedance(Impedance, ImpedanceSource=50, out="normal"):
    import numpy as np

    """
    If out is set to;
        normal, normalised impedace will be returned
        gamma, Reflection Coefficient with magnitude (0) and angle (1)
        S11, S-Parameters in dB    

    RF Example

    import Circuits as cct
    |
    |____
    |    |
    Z R5 |
    |    = C1
    3 L1 |
    |____|
    |
    L1 = 5e-9; C1 =3e-12; Z0 = 50
    F = 1e9; R5 = 75; ZL1 = 1j * F * L1; ZC1 = 1/ (1j * F * C1)
    Z = cct.parallel([R5 + ZL1, ZC1])

    print("Impedance =", Z)
    Znormal = cct.NormalisedImpedance(Z, Z0)
    print("Normalised Impedance =", Znormal)
    mag, ang = cct.NormalisedImpedance(Z, Z0, out = "gamma") # type: ignore
    print("Polar Normalised Impedance =",  mag ,"∠", ang, "°")
    S11 = cct.NormalisedImpedance(Z, Z0, out = "S11")
    print("S11 =",S11, "dB")
    ReturnLoss = cct.ReturnLoss(-1*S11)
    print("Return Loss =",ReturnLoss, "dB")
    """
    Zcoeff = (Impedance - ImpedanceSource) / (Impedance + ImpedanceSource)
    S11 = 20 * np.log10(abs(Zcoeff))
    if out == "normal":
        return Impedance / ImpedanceSource
    elif out == "gamma":
        return abs(Zcoeff), np.angle(Zcoeff, deg=True)
    elif out == "S11":
        return S11
    else:
        return """ERROR: please set 'out' to 
        normal, normalised impedace will be returned 
        gamma, gamma with magnitude (0) and angle (1) 
        S11, Input Reflection Coefficient with matched load in dB """

def Reflection2Impedance(Magnitude, Angle, ImpedanceSource=50, out="normal", ang="deg"):
    import numpy as np

    """
    If out is set to;
        normal, normalised impedace will be returned
        circuit, the circuit impedance will be returned 
        ang = "deg" for degrees (default) or  "rads" for radians 
    """
    rfcoeff = 0.0
    try:
        if ang == "deg":
            rfcoeff = Magnitude * np.exp(1j * Angle * np.pi / 180)
        if ang == "rads":
            rfcoeff = Magnitude * np.exp(1j * Angle)
    except:
        """ERROR: ang = "deg" for degrees (default) or  "rads" for radians"""
        raise
    ZNormal = (1 + rfcoeff) / (1 - rfcoeff)
    Z = ImpedanceSource * ZNormal
    if out == "normal":
        return ZNormal
    elif out == "circuit":
        return Z
    else:
        return """ERROR: please set 'out' to 
        normal, normalised impedace will be returned
        circuit, the circuit impedance will be returned  """

def P2R(radii, angles):
    import numpy as np
    return radii * np.exp(1j * angles)

def R2P(x):
    import numpy as np
    return abs(x), np.angle(x)

def ReturnLoss(S11):
    import numpy as np
    return -20 * np.log10(S11)

def VoltageDivider(V1:float, R1:float, R2:float):
    return V1 * ((R2) / (R2+R1))

def ThreePhase2SinglePhase(Vline):
    import numpy as np
    return Vline / np.sqrt(3)

def SinglePhase2ThreePhase(Vphase):
    import numpy as np
    return VPhase * np.sqrt(3)

def RMSVoltage(Vpeak):
    import numpy as np
    return (Vpeak/np.sqrt(2))
