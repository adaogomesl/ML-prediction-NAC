#!/bin/bash
#SBATCH --partition=short
#SBATCH --time=23:00:00
#SBATCH --output=%j.o.slurm
#SBATCH --error=%j.e.slurm

for i in 164 189 262 269; do
	source_file="dbh-${i}_energies.xyz"
	target_file="dbh-${i}_3D.xyz"
	output_file="data_dbh-${i}.xyz"

	# Read source lines into an array
	IFS=$'\n' read -d '' -r -a source_lines < "$source_file"

	# Initialize variables
	source_index=0
	source_count=${#source_lines[@]}

	# Prepare the output file
	> "$output_file"

	# Read the target file line by line
	while IFS= read -r line || [[ -n "$line" ]]; do
	    # Check if the line is blank
	    if [[ -z "$line" && $source_index -lt $source_count ]]; then
	        # Insert a line from the source file
	        echo "${source_lines[$source_index]}" >> "$output_file"
	        ((source_index++))
	    elif [[ -n "$line" ]]; then
	        echo "$line" >> "$output_file"
	    fi
	done < "$target_file"

	# Check if there are any remaining source lines
	while [ $source_index -lt $source_count ]; do
	    echo "${source_lines[$source_index]}" >> "$output_file"
    ((source_index++))
done
done


