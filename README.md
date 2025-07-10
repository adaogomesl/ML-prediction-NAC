# Details
This repository contains scripts and details related to:
1. Data extraction from CASSCF NAMD, which include energies, coordinates, forces and NACs.
2. Preprocessing data for
  a. SPAINN

# Data Extration 
_Observation: the files should be on trajectory folder obtained from dynamics_
1. Extract energies from *md.energies ```python3 extract_energy_training_data.py title```
2. Extract coordinates, forces and NACs ```python3 extract_energy_training_data.py title```

_Observation: both *energies.xyz and *3D.xyz should be in the same folder as the extraction script_ 
3. Combine data in one single file ```sbatch combined.sh```

# Preprocessing data
## Preprocessing data for SPaiNN
1. Run ```make_SPAINN_db.py``` in the same folder as the generated files on step 3 of data extraction

