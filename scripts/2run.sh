#!/bin/bash
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --account=def-daknox
#SBATCH --mail-user=architpandeynitk@gmail.com
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --job-name=2
#SBATCH --output=%x-%j.out

module avail python &> /dev/null
module load python/3.6.3 &> /dev/null
pip3 install -r requirements.txt --user &> /dev/null
python3 ./mitacs/ml/doc2vec.mod.py -c ./mitacs/data/Test/2_test.csv
