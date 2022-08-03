#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
Codename: pydos
Version: 1.0
Author: Zhaoxz
Email: xingzezhao9812@163.com
'''

# import #
from asyncore import write
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

def Input(filename,pltxlim):
    path = './' + filename + '.dat'
    with open(path,'r') as file:
        lines = file.readlines()
    Eng = []
    Englist = []
    Dos = []
    Doslist = []
    for l in lines:
        if l == '\n':
            if Eng == []:
                continue
            Englist.append(Eng)
            Doslist.append(Dos)
            Eng = []
            Dos = []
            continue
        en = float(l.strip().split()[0])
        dos = float(l.strip().split()[1])
        if en > -pltxlim and en < pltxlim:
            Eng.append(en)
            Dos.append(dos)
    
    return Englist, Doslist

filename = input('Type your input filename:')
pltxlim = float(input('Type the xlim(eV) of DOS image:'))
atomname = input('Type the name of atom, use BLANK key to separate them:')
ifsavedata = input('Would you like to save the data?(y/n)')

Eng, Dos = Input(filename,pltxlim)

atomname = atomname.strip().split()
atomname.insert(0,'Total')
atomname.insert(0,'Total')

plt.figure(figsize=(30,16))
color = ['#989998','#000000','#d35230','#7BB3D7','#D8A4F2','#C3D69B','#989998']
dossmth_list = []
for index in range(0,len(Eng)):
#     plt.plot(Eng[index],Dos[index],c = color[index], label = atomname[index])
    dos_smooth = scipy.signal.savgol_filter(Dos[index],7,3) 
    dossmth_list.append(dos_smooth)
    plt.plot(Eng[index],dos_smooth,c = color[index],label = atomname[index])
plt.xlim(-pltxlim*1.01,pltxlim*1.01)

# move the x axis to y = 0
ax = plt.gca()
ax.spines['right'].set_color('none') 
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data',0))

# label fontsize
plt.xlabel('Energy(eV)', fontsize = 18)
plt.ylabel('Density of States(states/eV)', fontsize = 18)
plt.tick_params(labelsize=16)  #刻度字体大小13

plt.legend(fontsize='xx-large')
# plt.ylim(-300,300)
savename = './' + filename + '.jpg'
plt.savefig(savename,dpi=500,bbox_inches="tight")

if ifsavedata == 'y':
    savedat = []
    savepath_total1 = './smoothdata/' + filename + '_tot1.dat'
    savedat.append(savepath_total1)
    savepath_total2 = './smoothdata/' + filename + '_tot2.dat'
    savedat.append(savepath_total2)
    for i in atomname[2:]:
        savepath_atm = './smoothdata/' + filename + '_' + i + '.dat'
        savedat.append(savepath_atm)

    for i in range(0,len(Eng)):
        savepath_w = savedat[i]
        with open(savepath_w, 'w') as file:
            for j in range(0, len(Eng[i])):
                file.write(str(Eng[i][j]))
                file.write('\t')
                file.write(str(dossmth_list[i][j]))
                file.write('\n')
            file.close()

