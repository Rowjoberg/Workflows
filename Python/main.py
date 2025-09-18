def main():

    from Circuits import parallel 
    R1 = 13e3
    R2 = 360e3
    R71 = 1.8e3
    R75 = 1.8e3
    R4 = 7.5e3
    R82 = 82
    
    R9 = 20e3
    R10 = 360e3
    R12 = 6.2e3
    RTpTwo2TpFour = 1592


    print("R2 Measurement = ",parallel([R1, R2, R4 + R71 + R75]),"Ohms")
    print("R10 Measurement = ",parallel([R9, R10, R12 + RTpTwo2TpFour]),"Ohms")

if __name__ == "__main__":
    main()
