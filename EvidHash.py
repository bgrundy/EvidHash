#! /usr/bin/env python3
# Script: EvidHash.py
# Author: Grundy, Barry J.
# Purpose:  
# - Provide a simple example of hashing EWF files in two ways
#   - The container files themselves using hashlib
#   - The data contained in the EWF files.
# Usage: EvidHash.py <filename.E01>
#    - You must provide the name of the first segment of the EWF list
#   - Only the first file of a set is required 
#   - The script currently works only on EWF files
# Changes:
# DONE:
# TODO:
# REQUIRES:
#   - hashlib
#   - pyewf
#   - tqdm (for progress bar)

Version = "0.1"

#####################################
#  Module imports                   #
#####################################
import sys
import pyewf
import hashlib
from tqdm import tqdm
from datetime import datetime

################################################################################
#   Function Definitions                                                       #
################################################################################

# Get the MD5sum of the container (EWF) files:
def getHash(flist):
    mdlist = []
    try:
        for segment in tqdm(flist):
            with open(segment,'rb') as ckhash:
                data = ckhash.read()
                hash = hashlib.md5(data).hexdigest()
                mdlist.append(str(segment)+": "+str(hash))
    except IOError:
        print("***Error opening "+segment+
          " - invalid file or file does not exist***")
        sys.exit(1)
    return mdlist

# Get the sizes (in bytes) of the container (EWF) files:
def getSize(flist):
    szlist = []
    try:
        for segment in tqdm(flist):
            with open(segment,'r') as fin:
                fin.seek(0,2) #for file size
                sz = fin.tell() #for file size
                szlist.append(str(segment)+" size = "+str(sz))
    except IOError:
        print("***Error opening "+segment+
          " - invalid file or file does not exist***")
        sys.exit(1)
    return szlist

# Get the media size and hash of the data contained in the EWF file:
def getewf_Info(flist):
    try:
        evid_obj=pyewf.handle()
        # Open the EWF files:
        evid_obj.open(flist)
        # Read the stored hash (data):
        hash=evid_obj.get_hash_value('MD5')
        # Read the stored media size:
        size=evid_obj.get_media_size()
    except:
        print("Unable to parse EWF files...")
        sys.exit(1)
    return hash,size

################################################################################
#   Main Program                                                               #
################################################################################

def main():
    try:
        # Read the command line arguments:
        print(len(sys.argv))
        print(sys.argv[1])
        arg_count = len(sys.argv)
        if arg_count < 2:
            print("Must provide the name of the first segment...")
            print("Try again.")
            sys.exit(1)
        if arg_count == 2:
            try:
                flist = pyewf.glob(sys.argv[1])
            except:
                print("Unable to open EWF files.")
                sys.exit(1)

        # Set the start time:
        starttime = datetime.strftime(datetime.now(),\
                       format='%b %d, %Y %H:%M:%S')
        print("Script Starting..."+starttime)
        print("Collecting evidence container file info...")
        md_list = getHash(flist)
        sz_list = getSize(flist)
        print("Collecting EWF info...")
        ewf_hash,ewf_sz = getewf_Info(flist)    
        endtime = datetime.strftime(datetime.now(),\
                       format='%b %d, %Y %H:%M:%S')
        # Print the output:
        print("Script complete: ")
        print("\nStart: ", starttime)
        print("\nContainer File Hashes:")
        for hash in md_list:
            print('\t',hash)
        print("Container File Sizes:")
        for size in sz_list:
            print('\t',size,"bytes")
        print("\nEWF stored MD5 hash: ", ewf_hash)
        print("EWF stored media size: ", ewf_sz, "bytes")
        print("\nEnd: ", endtime)
        sys.exit(0)

    except KeyboardInterrupt:
        print("Keyboard interrupt.  Exiting...")    
        sys.exit(1)

####################################################
#  Main program loop                               #
####################################################

if __name__ == '__main__':
    main()
