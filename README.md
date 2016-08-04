# Distance_matrix
This script computes the minimum distance for every residue pair within the protein for all the frames in the trajectory. Once all minimum distances are obtained, the distances are plotted in a contact map. The output is currently printed to three files within a designated directory for each trajectory: dist_calc.output, trajectory.system.avg_distance_matrix.dat and trajectory.system.std_distance_matrix.dat. The .output contains progress reports for the job that was run. The avg_distance_matrix.dat contains the average minimum distance for each residue pair for the entire trajectory. The std_distance_matrix.dat contains the standard deviation of the minimum distance for each residue pair for the entire trajectory. 

USAGE: sbatch submit_matrix_calc.sh

The submit_matrix_calc.sh will run ./matrix_calc.py pdb_file traj_loc start end system_descriptor

Once the matrix_calc.py file is completed, run the weighted_average.py script to that the weighted average of all the contact maps that were generated from the matrix_calc.py script.

NOTES: 
This python script requires MDAnalysis and numpy libraries.
The topology file is in a pdb format.
The trajectory file can be any trajectory format but the format that is used is a .dcd file.
   
