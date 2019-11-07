#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
##!/mnt/lustre_fs/users/mjmcc/apps/python2.7/bin/python
# ----------------------------------------
# USAGE:

# ----------------------------------------
# PREAMBLE:

import sys
import numpy as np
import os
from plotting_functions import *

# ----------------------------------------
# VARIABLE DECLARATION

descriptor = sys.argv[1]	# descriptor to decide which trajectory group to analyze for all systems

# description of sys_list.append(['velocity number','equilibrated portion of the system for that specific velocity number'])
sys_list = []
sys_list.append(['velocity.1','095.100','s411a_ssrna_atp_1'])
#sys_list.append(['velocity.2','010.027','wt_2'])
#sys_list.append(['velocity.3','017.027','wt_3'])


nSys = len(sys_list)

# ----------------------------------------
# SUBROUTINES:

# ----------------------------------------
# MAIN PROGRAM:

for i in range(nSys-1):
	avg1 = np.loadtxt('../../../%s/md/Distance_matrix/%s.%s.avg_distance_matrix.dat' %(sys_list[i][0],sys_list[i][1],sys_list[i][2]))
	std1 = np.loadtxt('../../../%s/md/Distance_matrix/%s.%s.std_distance_matrix.dat' %(sys_list[i][0],sys_list[i][1],sys_list[i][2]))

	nRes = len(avg1)

	for j in range(i+1,nSys):
		avg2 = np.loadtxt('../../../%s/md/Distance_matrix/%s.%s.avg_distance_matrix.dat' %(sys_list[j][0],sys_list[j][1],sys_list[j][2]))
		std2 = np.loadtxt('../../../%s/md/Distance_matrix/%s.%s.std_distance_matrix.dat' %(sys_list[j][0],sys_list[j][1],sys_list[j][2]))

		avg_data = avg1 - avg2
		std_data = std1 - std2

		out1 = open('AVG_dif.%s.%s.output' %(sys_list[i][0],sys_list[j][0]),'w')
		out2 = open('AVG_dif.%s.%s.hist.dat' %(sys_list[i][0],sys_list[j][0]),'w')
		count_array = np.zeros(nRes)
		for x in range(nRes-1):
			for y in range(x+1,nRes):
				if abs(avg_data[x][y]) > 5.0:
					out1.write('%s   %s   %03d (%d)   %03d (%d)   %f\n' %(sys_list[i][0],sys_list[j][0],x+1,x+8,y+1,y+8,avg_data[x][y]))
					count_array[x] += 1
					count_array[y] += 1
		for x in range(nRes):
			out2.write('%03d   %03d   %d\n' %(x+1,x+8,count_array[x]))

		out1.close()
		out2.close()

		bar(range(nRes),count_array[:],'Residue Number', 'Freq of large changes in Contact', '%s.%s.%s' %(descriptor,sys_list[i][0],sys_list[j][0]),'difference_avg',x_lim=(0,nRes),y_lim=(0,257))
		matrix2d(abs(avg1-avg2),'Residue Number','Residue Number','Distance','%s.%s.%s' %(descriptor,sys_list[i][0],sys_list[j][0]),'difference_avg',cb_units='$\AA$',vmax=8.)
		matrix2d(abs(std1-std2),'Residue Number','Residue Number','Distance','%s.%s.%s' %(descriptor,sys_list[i][0],sys_list[j][0]),'difference_std',cb_units='$\AA$',vmax=1.5)

