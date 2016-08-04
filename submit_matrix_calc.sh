#!/bin/bash
#SBATCH --job-name=dist_cal.wt_1
#SBATCH --output=dist_cal.wt_1.output
#SBATCH --time=96:00:00 
#SBATCH --nodes=1
#SBATCH --exclusive

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/software/usr/gcc-4.9.2/lib64"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/software/usr/hpcx-v1.2.0-292-gcc-MLNX_OFED_LINUX-2.4-1.0.0-redhat6.6/ompi-mellanox-v1.8/lib"

export PYTHON_EGG_CACHE="./"

PDB_LOC='/mnt/lustre_fs/users/dupontke/research/3evg/wt/velocity.1/md/traj/truncated.pdb'
TRAJ_LOC='/mnt/lustre_fs/users/dupontke/research/3evg/wt/velocity.1/md/traj/Truncated/'
SYSTEM='wt_1'
NPRODS=27
NCPUS=20

prod=1
for ((i=1;i<=2;i++))
do
	j=1
	while ((j <= $NCPUS)) && ((prod <= $NPRODS))
	do
		echo $j $i $prod
		((a=$prod))
		printf -v x "%03d" $prod
		printf -v y "%03d" $a
		mkdir $x.distance_matrix
		cd $x.distance_matrix
		time /mnt/lustre_fs/users/mjmcc/apps/python2.7/bin/python ../matrix_calc.py $PDB_LOC $TRAJ_LOC $prod $a $SYSTEM > dist_calc.output & 
		cd ../
		((j=$j+1))
		((prod=$prod+1))
	done
	wait
done

