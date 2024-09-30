import os

from model.bitstream import Bitstream
from model.item_data import Item
from saf_writer.generate_saf import generate_saf

item = Item()


def process_rows(input_values: list, directory: str, saf_directory: str, alt_bundle: str):
    """
    Reads the file input one line at a time to process item and bitstream
    information. Calls the generate SAF function for individual items.

    :param input_values: A list of dictionaries generated from the input csv file.
    :param directory: The input directory containing the csv and bitstream files
    :param saf_directory: The output SAF directory
    :param alt_bundle: if provided image bitstreams will be added to this bundle
    :return: void
    """

    create_output_saf_directory(saf_directory)

    previous_row = None

    length = len(input_values)
    row_count = 1
    item_count = 1

    # Iterate through each row in the input file
    for row in input_values:

        if row_count == 1:
            # add metadata for first row
            process_item(row, item)
            process_bitstream(row, item)
        elif previous_row is not None:
            # if the next row is an item, generate saf and add metadata to new item
            if row['dc.title'].strip():
                generate_saf(item, directory, saf_directory, item_count, alt_bundle)
                item_count += 1
                item.reset()
                process_item(row, item)
                process_bitstream(row, item)
            # if it's image metadata, add it to current item
            else:
                # process_item(row, item)
                process_bitstream(row, item)

        if row_count == length:
            # if last row just generate the saf
            generate_saf(item, directory, saf_directory, item_count, alt_bundle)

        # Update previous_row to be the current row
        previous_row = row
        row_count += 1


def process_bitstream(row, current_item):
    bit = Bitstream()
    for key in row.keys():
        if key in Bitstream.bitstream_labels:
            if len(row[key].strip()) > 0:
                bit.set_value(key, row[key])
    if bit.get_value('Filename') is not None:
        current_item.add_bitstream(bit)


def process_item(row, current_item):
    for key in row.keys():
        if key not in Bitstream.bitstream_labels:
            if len(row[key].strip()) > 0:
                current_item.set_value(key, row[key])


def create_output_saf_directory(saf_directory):
    os.mkdir(saf_directory)
