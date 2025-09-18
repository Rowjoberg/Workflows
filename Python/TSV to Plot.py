import pandas as pd
import matplotlib.pyplot as plt

r_filenameTSV = 'G:/My Drive/Uni/ELEC3240/Lab 2/Lab_1_Q5.tsv'
tsv_read = pd.read_csv(r_filenameTSV, sep='\t')
print(tsv_read)
R2 = tsv_read.loc[:, 'r2']
# print(R2)
I = tsv_read.loc[:, 'I(R2)']
print(I)
V = tsv_read.loc[:, 'V(n002)']
print(V)

fig, ax = plt.subplots()
ax.plot(I*10e5, V)

ax.set(xlabel='Current (uA)', ylabel='Voltage (V)',
       title='Load Current vs Load Voltage')
ax.grid()

fig.savefig("G:/My Drive/Uni/ELEC3240/Lab 2/Q5.png")
plt.show()