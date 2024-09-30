import argparse
from csv import DictReader

from processor.process_rows import process_rows


def process_input(parent_directory, saf_directory, alt_bundle):

    input_file = parent_directory + '/' + 'input.csv'

    # Open the input CSV file for reading
    with open(input_file, mode='r', newline='') as infile:
        reader = DictReader(infile)
        # creates a list of dictionaries
        list_of_dict = list(reader)
        process_rows(list_of_dict, parent_directory, saf_directory, alt_bundle)


parser = argparse.ArgumentParser(
    description='Convert a directory containing a csv metadata file and bitstreams to DSpace Simple Archive Format.')

parser.add_argument('dir', metavar='Parent directory', type=str,
                    help='full path to the directory (you can omit the final "/")')
parser.add_argument('saf', metavar='Output SAF directory', type=str,
                    help='full path to the output directory that will contain the SAF subdirectories')
parser.add_argument('-b',  "--bundle",
                    help='images can be added to an alternate bundle if you do not want them included in the default '
                         '(ORIGINAL) bundle')
args = parser.parse_args()

directory = args.dir
saf = args.saf

process_input(directory.rstrip('/'), saf.rstrip('/'), args.bundle)
