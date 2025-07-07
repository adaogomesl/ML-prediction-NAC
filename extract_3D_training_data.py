import sys, os
import numpy as np

### Updated by: Leticia A. Gomes on July 7 2025
### Goal: Extract coordinates, forces and NACs results from Molcas/PyRAI2MD NAMD *.log for ML Training 
### Usage: python3 extract_3D_training_data.py title

def MolcasCoord(M):
	coord = []
	for line in M:
		a, x, y, z = line.split()[0:4]
		coord.append([a, float(x), float(y), float(z)])
	return coord
def S2F(M):
## This function convert 1D string (e,x,y,z) list to 2D float array

	M = [[float(x) for x in row.split()[1: 4]] for row in M]
	return M

def flatten(nested_lists):
	return [i for sub_lis in nested_lists for in_lis in sub_lis for i in in_lis]

def scrape_data(file_name,natom,output_file):
	with open(file_name, 'r') as out:
		log = out.read().splitlines()
	nac      = []
	coord    = []
	gradient1 = []
	gradient2 = []
	accord   = []
	
	for i, line in enumerate(log):
		if   """&coordinates in Angstrom""" in line:
			coord = log[i + 2: i + 2 + natom]
			coord = MolcasCoord(coord)
			accord.append(coord)
		elif """&gradient state               1 in Eh/Bohr""" in line:
			g1 = log[i + 2: i + 2 + natom]
			g1 = S2F(g1)
			gradient1.append(g1)
			
		elif """&gradient state               2 in Eh/Bohr""" in line:
			g2 = log[i + 2: i + 2 + natom]
			g2 = S2F(g2)
			gradient2.append(g2)

		elif """&nonadiabatic coupling   1 -   2 in Hartree/Bohr M = 1 / 1""" in line:
			n = log[i + 2: i + 2 + natom]
			n = S2F(n)
			nac.append(n)

	gradient1 = [[[-x for x in atom] for atom in frame] for frame in gradient1]
	gradient2 = [[[-x for x in atom] for atom in frame] for frame in gradient2]

	output_file_path = os.path.join(data_ml_training_folder, output_file)
	with open(output_file_path,'w') as f:
		for i in range(2000):
			f.write(str(natom)+'\n'+'\n')
			for j in range(natom):
				f.write(f"{accord[i][j][0]:<2} {accord[i][j][1]: .16f} {accord[i][j][2]: .16f} {accord[i][j][3]: .16f} {nac[i][j][0]: .16f}  {nac[i][j][1]: .16f} {nac[i][j][2]: .16f} {gradient1[i][j][0]: .16f}  {gradient1[i][j][1]: .16f} {gradient1[i][j][2]: .16f} {gradient2[i][j][0]: .16f}  {gradient2[i][j][1]: .16f} {gradient2[i][j][2]: .16f}\n")


title='%s' % sys.argv[1].split('.')[0]

base_folder = os.getcwd()


data_ml_training_folder = os.path.join(base_folder, 'data_3D_ML_training')
os.makedirs(data_ml_training_folder, exist_ok=True)
    
for folder_name in os.listdir(base_folder):
    if title in folder_name:
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.exists(folder_path):
            file_name=folder_name+'.log'
            file_path = os.path.join(folder_path,file_name)
            scrape_data(file_path,15,folder_name+'_3D.xyz')
