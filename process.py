import os
import glob
from subprocess import check_call
import sys
import argparse

parser = argparse.ArgumentParser(description="pre-process dataset")
parser.add_argument("-p", "--prefix", default=None, 
        help="specify the prefix to add to all the pcap files")
parser.add_argument("-f", "--folder", default=None,
        help="specify the folder to look for dataset")

args = parser.parse_args()

if args.prefix:
    pre_name = args.prefix
else:
    pre_name = "p"
if args.folder:
    f_name = args.folder
else:
    parser.print_help()

for zipped_file_name in glob.glob(os.path.join(f_name, "*.7z")):
    print("--> start to process 7z_file: [%s]"%(zipped_file_name))
    cmd = "p7zip -d %s" % (zipped_file_name)
    check_call(cmd, shell=True)

for pcap_file_name in glob.glob(os.path.join(f_name, "*.pcap")):
    print("--> start to process pcap_file: [%s]"%(pcap_file_name))
    cmd = "mv %s %s" % (pcap_file_name, pre_name + "_"
            + pcap_file_name.rsplit('/')[-1])
    check_call(cmd, shell=True)
