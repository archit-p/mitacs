'''
A simple script to pre-process the dataset
'''

import os
import glob
from subprocess import check_call
import sys
import argparse

'''
Parse the command line arguments
'''

parser = argparse.ArgumentParser(description="pre-process dataset")
parser.add_argument("-p", "--prefix", default=None, 
        help="specify the prefix to add to all the pcap filenames")
parser.add_argument("-f", "--folder", default=None,
        help="specify the folder to look for dataset")

args = parser.parse_args()

if args.prefix:
    pre_name = args.prefix
else: 
    parse.print_help()
if args.folder:
    f_name = args.folder
else:
    parser.print_help()

'''
If file exists as a 7z file, extract it
'''

for zipped_file_name in glob.glob(os.path.join(f_name, "*.7z")):
    print("--> start to process 7z_file: [%s]"%(zipped_file_name))
    cmd = "p7zip -d %s" % (zipped_file_name)
    check_call(cmd, shell=True)

'''
Convert the pcap files into the right filename format
'''
for pcap_file_name in glob.glob(os.path.join(f_name, "*.pcap")):
    print("--> start to process pcap_file: [%s]"%(pcap_file_name))
    if(pre_name != ""):
        cmd = "mv %s %s" % (pcap_file_name, pre_name + "_"
                + pcap_file_name.rsplit('/')[-1])
    else:
        cmd = "mv %s %s", % (pcap_file_name, 
                pcap_file_name.rsplit('/')[-1])
    check_call(cmd, shell=True)
