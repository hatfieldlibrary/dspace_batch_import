Batch imports for DSpace use the Simple Archive Format (SAF). This code is used to create SAF import directories from a csv file.

The program input is a subdirectory that contains the csv file and bitstreams. The output are SAF subdirectories that contain dublin core metadata,
a contents file listing bitstreams and bitstream metadata, and optional iiif and local metadata files.

```usage: read_input.py [-h] [-b BUNDLE] Parent directory Output SAF directory

Convert a directory containing a csv metadata file and bitstreams to DSpace Simple Archive Format.

positional arguments:
  Parent directory      full path to the directory (you can omit the final "/")
  Output SAF directory  full path to the output directory that will contain the SAF subdirectories

optional arguments:
  -h, --help            show this help message and exit
  -b BUNDLE, --bundle BUNDLE
                        images can be added to an alternate bundle if you do not want them included in the default (ORIGINAL) bundle```
