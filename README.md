# EvidHash
This program is a simple example of utilizing a couple of libraries to
provide evidence hashing in python scripts.

This particular script works with Expert Witness Files, but the fuctions
can be adjusted for raw/split files as well.

It is provided for conceptual purposes only and can easily be simplified
or adjusted for production use.

Note that we use only MD5 in this script as it is meant to check the
itegrity of the file after a move across a network or to a new volume.
We are not concerned with collisions here, and this is not meant to take
the place of evidentiary control and integrity checks, only logistical
moves.  Also note that the libewf library currently only uses MD5
anyway.

## Functions

There are three main functions that do the work here.  All three take
`flist` as an argument.  `flist` is simply a python list of the EWF
segments being processed.  The list is created using the `pyewf`
library `glob` function - so only the first segment of the EWF set needs
to be passsed to the script.

### `getHash()`

This function provides a list of all the MD5 hashes of the container files.

### `getSize()`

This function provides a list of all the sizes (in bytes) of the container files.

### `getewf_Info()`

This function obtains the stored hash and media size of the data
contained in the EWF set.
