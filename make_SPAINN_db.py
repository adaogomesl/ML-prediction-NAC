import numpy as np
from ase import Atoms
from ase.db import connect
import os

"""
Purpose: Converted extract data from Molcas or PyRAI2MD NAMD dynamics into a ASE DB.
         Making data more compact and more convenient.

Usage: python make_ase_db.py

Assumptions: You should have extracted the data(follow tutorial for details) and correct the NACs phase

Author: Leticia Gomes
Date: May 30, 2025

"""

#Convertion factor
ANGSTROM_TO_BOHR = 1.0 / 0.529177 ########## use ASE conversion 

def get_coupling_index(i, j, n_states):
    return i * n_states - (i * (i + 1)) // 2 + j - i - 1

def parse_custom_xyz(filename, max_frames):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f]

    #Define variables   ########## Make automatic - Maybe ask user on command line ?
    nsinglets=2
    ntriplets = 0
    nstates = nsinglets + ntriplets
    db_name = "dbh_8k.db"
    db = connect(db_name)
    
    #Create dictionary to store properties
    keys=['energy','nacs','forces']    
    datas={}
    for key in keys:
        datas[key]=[]
    atoms_list = []
    i = 0
    frame_count = 0

    while i < len(lines) and frame_count < max_frames:
        if not lines[i].strip().isdigit():
            i += 1
            continue

        n_atoms = int(lines[i].strip()) #Get number of atoms
        header = lines[i + 1].strip() #Get trajectory number 
        atom_lines = lines[i + 2 : i + 2 + n_atoms]# Make a list with vector properties values (XYZ, forces and NACs).
        #On atoms_lines, each line is a element of the list


        # Energies
        energies = np.zeros((nstates,1))
        energy_tokens = [t for t in header.split() if "Epot_state" in t]
        energies_list = [float(t.split('=')[1]) for t in energy_tokens]
        for j in range(nstates):
            energies[j] = energies_list[j]
        datas["energy"]=energies.reshape(-1)
        
            
        n_couplings = nstates * (nstates - 1) // 2
        symbols, positions = [], []
        force1, force2, nac = [], [], [] #Needs to be modified if more states are considered ##########

        for line in atom_lines:
            parts = line.split()
            symbols.append(parts[0])
            positions.append([float(x) for x in parts[1:4]])
            nac.append([float(x) for x in parts[4:7]])
            force1.append([float(x) for x in parts[7:10]])
            force2.append([float(x) for x in parts[10:13]])
            

        positions = np.array(positions) * ANGSTROM_TO_BOHR    

        #NACs
        nacs = np.zeros((n_couplings,n_atoms,3))
        for l in range(n_couplings):
            for iatom in range (n_atoms):
                for xyz in range(3):
                    nacs[l][iatom][xyz]=nac[iatom][xyz]
        datas["nacs"]=nacs

        #Forces
        forces = np.zeros((nstates,n_atoms,3))
        
        for iatom in range (n_atoms):
            for xyz in range(3):
                forces[0][iatom][xyz]=force1[iatom][xyz]
                forces[1][iatom][xyz]=force2[iatom][xyz]
        datas["forces"]=forces
        

        atoms = Atoms(symbols=symbols, positions=positions)
        db.write(atoms,data=datas)
        
        atoms_list.append(atoms)
        i += 2 + n_atoms
        frame_count += 1
        
    metadata = {}
    #metadata["info"]="Metada information for "
    # this information is required
    #metadata['system']='Cyclopropenone'
    metadata["n_singlets"]=nsinglets
    metadata["n_triplets"]=ntriplets
    metadata["states"]='S S S'
    metadata["phasecorrected"]=False
    metadata["ReferenceMethod"]="SA(4)-CASSCF(8,9)/ANO-S-VDZP, program: OpenMolcas and Pyrai2MD"
    metadata["atomrefs"]={}
    #metadata["_distance_unit"]="Bohr"
    #metadata["_property_unit_dict"]="{'energy': 'Hartree', 'forces': 'Hartree/Bohr', 'nacs': '1'}"
    db.metadata=metadata

    return db

def main():
    db_name = "dbh_8k.db"
    
    for xyz_file in os.listdir('.'):           
        if xyz_file.startswith("data_dbh") and xyz_file.endswith(".xyz"):
            print(f"🔁 Writing {xyz_file} to {db_name} in ASE db formating...")
            db=parse_custom_xyz(xyz_file, max_frames=2000)


    print(f"✅ Done. Database written to {db_name}")

    print("We have ", len(db), " data points.")

    data=db.get(1).data
    for key in data:
        print(key,"shape:",data[key].shape)

    print(db.metadata)


if __name__ == "__main__":
    main()

