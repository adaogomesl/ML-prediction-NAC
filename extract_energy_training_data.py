import sys,os

### Create by: Leticia A. Gomes on June 7 2024
### Last Update: July 7, 2025 
### Goal: Extract Energies results from Molcas/PyRAI2MD NAMD #.md.energies for ML Training 
### Usage: python3 extract_energy_training_data.py title

title='%s' % sys.argv[1].split('.')[0]

# Define the base folder path where the folders are located
base_folder = os.getcwd()

# Create a directory named 'data_ML_training' within the base folder if it doesn't exist
data_ml_training_folder = os.path.join(base_folder, 'data_energies_ML_training')
os.makedirs(data_ml_training_folder, exist_ok=True)

# Define a function to convert the number to valid Python scientific notation
def convert_to_float(string_number):
    if 'D' in string_number:
        mantissa, exponent = string_number.split('D')
        scientific_notation = f"{mantissa}E{exponent}" # Convert the parts to float and concatenate them with 'E' as the exponent indicator
        return float(scientific_notation) # Convert the scientific notation string to a float
    else:
        return float(string_number)

# Iterate over each folders 
for folder_name in os.listdir(base_folder):
    if title in folder_name:
        folder_path = os.path.join(base_folder, folder_name)

        # Check if the folder exists
        if os.path.exists(folder_path):
            # Define the file path within the current folder
            file_name=folder_name+'.md.energies'
            file_path = os.path.join(folder_path,file_name)
            print(file_path)
        
        # Initialize the data structure for each folder
        data = {
            'timestep': [],
            'state':[],
            'Epot_current': [],
            'Epot_state0': [],
            'Epot_state1': [],
            'Epot_state2': [],
            'Epot_state3': []
        }
        
        # Open the file and process the data
        with open(file_path, 'r') as file:
            # Skip the first line
            next(file)
            
            # Process each subsequent line
            for line in file:
                columns = line.split()
                epopstates = [convert_to_float(col) for col in columns[4:8]]  # Convert each Epopstate value
                Epotcurrent=convert_to_float(columns[1])
                data['timestep'].append(float(columns[0]))
                data['Epot_current'].append(Epotcurrent)
                data['Epot_state0'].append(epopstates[0])
                data['Epot_state1'].append(epopstates[1])
                data['Epot_state2'].append(epopstates[2])
                data['Epot_state3'].append(epopstates[3])
                # Check State of Epot-current
                state_current=epopstates.index(Epotcurrent)  # Index of the matching Epopstate
                data['state'].append(state_current)
        
        # Save the processed data into a text file
        
        output_name=folder_name+'_energies.xyz'
        output_file_path = os.path.join(data_ml_training_folder, output_name)
        with open(output_file_path, 'w') as output_file:
            # Iterate over each index
            for j in range(len(data['timestep'])):
                # Write the data for each index in the desired format
                output_file.write(f"timestep={data['timestep'][j]:.2f} " f"state={data['state'][j]} " f"Epot_state0={data['Epot_state0'][j]:.16f} "  f"Epot_state1={data['Epot_state1'][j]:.16f} " f"Epot_state2={data['Epot_state2'][j]:.16f} " f"Epot_state3={data['Epot_state3'][j]:.16f}\n")

