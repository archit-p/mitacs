#!/bin/bash
#Bash script to automatically schedule the jobs
#Script checks for whether:
#	- an output file exists
#	- a job is already scheduled
#If both are false, it schedules a new job


for i in 8 9 10 11 12 13 14
do
	if ls ./$i*.out &> /dev/null || [[ $(squeue -u architp -n $i) ]]; then
			echo "Skipping $i"
	else
		sbatch $i"run.sh"
	fi
done
