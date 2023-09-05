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
#   - 0.3: Consolidated size read to one function
#   - 0.2: Added verification of data stored in EWF files
# REQUIRES:
#   - hashlib
#   - pyewf
#   - tqdm (for progress bar)
#   - termcolor (for verification message)

Version = "0.3"

#####################################
#  Module imports                   #
#####################################
import sys
import pyewf
import hashlib
from tqdm import tqdm
from termcolor import colored
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

# Get the media size and hash recorded in the EWF file:
def getewf_Info(flist):
    try:
        evid_obj=pyewf.handle()
        # Open the EWF files:
        evid_obj.open(flist)
        # Read the stored hash (data):
        stored_hash=evid_obj.get_hash_value('MD5')
        # Read the stored media size:
        size=evid_obj.get_media_size()
        # Close the EWF files:
        evid_obj.close()
    except:
        print("Unable to parse EWF files...")
        sys.exit(1)
    return stored_hash,size

# Calculate the hash of the data stored in the EWF files:
def calcewf_Hash(flist, sz):
    try:
        evid_obj=pyewf.handle()
        # Open the EWF files:
        evid_obj.open(flist)
        # Read the data from the EWF files into an iterable
        # so we can use tqdm for progress during hash
        data=[evid_obj.read(sz)]
        # Hash the data from the EWF files:
        for data in tqdm(data):
            data_hash=hashlib.md5(data).hexdigest()
        # Close the EWF files:
        evid_obj.close()
    except:
        print("Unable to parse EWF files...")
        sys.exit(1)
    return data_hash

################################################################################
#   Main Program                                                               #
################################################################################

def main():
    try:
        # Read the command line arguments:
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
        # List of md5sums for the segments:
        md_list = getHash(flist)
        # List of the sizes for the segments:
        sz_list = getSize(flist)
        print("Collecting EWF info...")
        # Get the stored hash and media size:
        ewf_stor_hash,ewf_sz = getewf_Info(flist)    
        print("\nCalculating the hash of the data...")
        # Calculate the hash of the data in the EWF files:
        ewf_data_hash = calcewf_Hash(flist, ewf_sz)
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
        print("EWF stored media size: ", ewf_sz, "bytes")
        print("\nEWF stored MD5 hash:\t ", ewf_stor_hash)
        print("EWF data MD5 hash:\t ", ewf_data_hash)
        # Hash comparison:
        if ewf_stor_hash == ewf_data_hash:
            print(colored("Hash Match:  EWF files VERIFIED","green"))
        else:
            print(colored("HASH MISMATCH: Data error or corruption!",
                          "red"))
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
