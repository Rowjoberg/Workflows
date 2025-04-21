"""
Test limits calculation for the IPM2 CPU Test
Based on jig schematics here:
http://subversion/svn/csm/projects/ipm/trunk/IPM%20Test%20Jig%20documentation/CPU%20Board/Hardware

"""
from math import pi
from random import random
import cmath


# Input parameters:
# Change frequency and V_in to get test limits based on the injected signal
frequency = 50.0 # Hz
V_in = 0.3493 # RMS voltage 
w = 2*pi*frequency
print(f"Injected: {V_in} Vrms")

def alter(value, tolerance):
    # Pick component value from a uniform distribution over a tolerance:
    rand = random() * 2 - 1 # Get a random float between -1 and 1
    return value + value * rand * tolerance # Map to a tolerance

def calculate_OL_current():
    # This function does the input to output mapping for each gain on the IPM2 processor board
    # Specifically the OL phase current measurements.

    # ----- JIG COMPONENTS -----
    Rjigtol = 0.01 # 1% resistors are used in the jig CHANGE ME IF YOU WANT SOME TOLERANCES
    R_mux = 40*0 # DG408 typical on resistance
    R89 = alter(100e3, Rjigtol) # ohms
    R90 = alter(820, Rjigtol) + R_mux
    R91 = alter(1.5e3, Rjigtol) + R_mux
    R92 = alter(3.3e3, Rjigtol) + R_mux
    R93 = alter(6.8e3, Rjigtol) + R_mux
    R94 = alter(15e3, Rjigtol) + R_mux
    R95 = alter(33e3, Rjigtol) + R_mux
    R96 = alter(100e3, Rjigtol) + R_mux

    def U14_scaling(gain_resistor):
        # Effect of U14 in the jig (SineIn --> SINE_SCALED on sch):
        return gain_resistor / (gain_resistor + R89)
        

    # ------ IPM2 COMPONENTS ----
    Ctol = 0.1 # 10% tolerance
    Rtol = 0.01 # 1% tolerance
    # IA_OL: (the other amplifiers are the same)
    C1 = alter(1e-6, Ctol) # 1uf
    R16 = alter(10e3,Rtol) # 10k
    R_wire = alter(0.01, 0) + R_mux # Wire resistance for 0 gain
    R37 = alter(12.4e3, Rtol) + R_mux # 12.4k
    R39 = alter(24.9e3, Rtol) + R_mux # 24.9k
    R43 = alter(49.9e3, Rtol)+ R_mux
    R40 = alter(100e3, Rtol) + R_mux
    R48 = alter(200e3, Rtol) + R_mux
    R52 = alter(402e3, Rtol) + R_mux
    R60 = alter(806e3, Rtol) + R_mux
    C38 = alter(1e-9, 0.05) # 1nF 5%
    R23 = alter(1e3, Rtol)
    C52 = alter(1e-6, Ctol)
    # Cap impedances:
    ZC1 = 1/(1j*w*C1)
    ZC38 = 1/(1j*w*C38)
    ZC52 = 1/(1j*w*C52)
    
    # Amplifier IA1_IN --> IA_OL
    ZC1_R16 = R16 + ZC1 # Impedance of C1, R16, add in R_mux from jig DG408 here too
    ZR23_p_C52 = ZC52/(ZC52 + R23) # Impedance of R23 and C52

    def U5_amp_gain(gain_resistor):
        # Compute gain over U5 amplifier
        feedback_impedance = 1/( 1/gain_resistor + 1/ZC38 )
        gain = (feedback_impedance / ZC1_R16) * ZR23_p_C52
        return gain 


    # Final calculation of input --> output:

    # This loop matches the way the test code applies each jig and DUT gain resistor:
    ipm_gain_resistors = [R_wire, R37, R39, R43, R40, R48, R52, R60]
    jig_gain_resistors = [10e12, 10e12, 10e12, R96, R95, R94, R93, R92]
    output_values = []
    for jig_gain, ipm_gain in zip(jig_gain_resistors, ipm_gain_resistors):
        # Get the gains
        jig_gain = U14_scaling(jig_gain)
        jig_output_voltage = V_in * jig_gain


        ipm_gain = U5_amp_gain(ipm_gain)
        v_out = jig_output_voltage * ipm_gain 
        output_values.append(cmath.polar(v_out)[0])

    return output_values


if __name__ == '__main__':
    outputs = [[],[],[],[],[],[],[],[]] 

    for i in range(1, 100000):
        # Every call to calculate will sample the component values from the distribution
        values = calculate_OL_current()
        for idx, value in enumerate(values):
            outputs[idx].append(value)
            
    # Have a look at the results
    vref = 4.096 # ADC Reference voltage
    adc_per_volt = (2**12 - 1) / vref # 12-bit ADC
    minimums = []
    maximums = []
    averages = []

    print("OL current ADC test limits:")
    for idx, value in enumerate(outputs):
        minimums.append(min(value))
        maximums.append(max(value))
        averages.append(sum(value) / len(value))
        
        v_peak_low = (min(value) * 2**0.5)
        v_peak_high = (max(value) * 2**0.5) 
        avg_pk = ( (sum(value) * 2**0.5) / len(value))
        avg = ( (sum(value)) / len(value))
        # Lef shift by 4? --> 12 bit adc, stored as left aligned 16 bit int in the test code
        adc_low = int((((2/pi) * v_peak_low) * adc_per_volt)) << 4
        adc_high = int((((2/pi) * v_peak_high) * adc_per_volt)) << 4
        adc_avg = int((((2/pi) * avg_pk) * adc_per_volt)) << 4
        
        print(f"G{idx} (low, mid, high): {adc_low}, {adc_avg}, {adc_high}       Vrms: {avg:.4f}")