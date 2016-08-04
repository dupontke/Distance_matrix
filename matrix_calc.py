#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
##!/mnt/lustre_fs/users/mjmcc/apps/python2.7/bin/python
# ----------------------------------------
# USAGE:

# ./matrix_calc.py pdb_file traj_loc start end system_descriptor

# ----------------------------------------
# PREAMBLE:

import sys
import numpy as np
from numpy.linalg import *
import MDAnalysis
import MDAnalysis.analysis.distances
from distance_functions import *

# ----------------------------------------
# VARIABLE DECLARATION

pdb_file = sys.argv[1]
traj_loc = sys.argv[2]
start = int(sys.argv[3])
end = int(sys.argv[4])
system = sys.argv[5]

zeros = np.zeros
square = np.square
sqrt = np.sqrt
flush = sys.stdout.flush

important = 'protein'

# ----------------------------------------
# SUBROUTINES:

def ffprint(string):
	print '%s' %(string)
	flush()

# ----------------------------------------
# MAIN PROGRAM:

u = MDAnalysis.Universe(pdb_file)
u_important = u.select_atoms(important)

nRes = len(u_important.residues)
ffprint(nRes)

res_list = []
for i in range(nRes):
	res_list.append(u_important.residues[i].select_atoms('not name H*'))
	res0 = res_list[i].positions

avg_matrix = zeros((nRes,nRes))
std_matrix = zeros((nRes,nRes))

nSteps = 0
while start <= end:
	ffprint('Loading trajectory %s' %(start))
	u.load_new('%sproduction.%s/production.%s.dcd' %(traj_loc,start,start))
	nSteps += len(u.trajectory)

	for ts in u.trajectory:
		if ts.frame%1000 == 0:
			ffprint('Working on timestep %d of trajectory %d' %(ts.frame, start))

		for i in range(nRes-1):
			res0 = res_list[i].positions
			for j in range(i+1,nRes):
				res1 = res_list[j].positions
				min_dist = 9999.
				for k in range(len(res_list[i])):
					atom0 = res0[k]
					for m in range(len(res_list[j])):
						atom1 = res1[m]
						dist, dist2 = euclid_dist(atom0,atom1)
						if dist < min_dist:
							min_dist = dist
				avg_matrix[i,j] += min_dist
				std_matrix[i,j] += min_dist*min_dist
	start +=1

ffprint(nSteps)

avg_matrix /= nSteps
std_matrix /= nSteps
std_matrix = sqrt(std_matrix - square(avg_matrix))

out1 = open('%03d.%03d.%s.avg_distance_matrix.dat' %(int(sys.argv[3]),end,system),'w')
out2 = open('%03d.%03d.%s.std_distance_matrix.dat' %(int(sys.argv[3]),end,system),'w')
for i in range(nRes):
	for j in range(nRes):
		out1.write('%10f   ' %(avg_matrix[i,j]))
		out2.write('%10f   ' %(std_matrix[i,j]))
	out1.write('\n')
	out2.write('\n')
out1.close()
out2.close()

