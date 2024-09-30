import os
import shutil
import xml.etree.cElementTree as ET

from model.item_data import Item


def generate_saf(item: Item, input_directory: str, saf_directory: str, count: int, alt_bundle: str):
    """
    Creates a new SAF subdirectory for an item. The subdirectory will
    contain the contents and dublin_core metadata as well as bitstreams.
    It may optionally contain iiif and local metadata.

    :param item: The object containing the metadata fields and list of
    bitstreams for an item.
    :param input_directory: The path to the input directory containing the
    csv file and bitstreams.
    :param saf_directory: The location of the SAF output directory
    :param count: The number of the items processed. Used to name the
    SAF subdirectory for the item.
    :param alt_bundle: If provided, image bitstreams are added to this bundle

    :return: void
    """

    # create the saf subdirectory for this item.
    saf_sub_directory = saf_directory + '/' + f"{count:04}"
    os.mkdir(saf_sub_directory)

    # get this list of bitstreams for the item
    bits = item.get_value('bitstreams')
    # create the 'contents' file for this subdirectory
    contents_file = open(saf_sub_directory + '/contents', 'a')
    # copy bitstreams to the output saf subdirectory and add the file names to contents
    for bit in bits:
        file = bit['Filename']
        file_name = file
        if alt_bundle and check_extension(file):
            file_name = file_name + '\tbundle:' + alt_bundle
        if bit['iiif.label']:
            file_name = file_name + '\tiiif-label:' + bit['iiif.label']
        if bit['iiif.description']:
            file_name = file_name + '\tiiif-description:' + bit['iiif.description']
        if bit['iiif.toc']:
            file_name = file_name + '\tiiif-toc:' + bit['iiif.toc']
        shutil.copyfile(input_directory + '/' + file, saf_sub_directory + '/' + file)
        contents_file.write(file_name + '\n')
    contents_file.close()

    # dublin core metadata
    root = ET.Element("dublin_core")
    for key in item.data:
        if key.startswith('dc.'):
            if item.data[key]:
                elems = key.split('.')
                if len(elems) == 3:
                    ET.SubElement(root, "dcvalue", element=elems[1], qualifier=elems[2]).text = item.data[key]
                else:
                    ET.SubElement(root, "dcvalue", element=elems[1]).text = item.data[key]
    tree = ET.ElementTree(root)
    tree.write(saf_sub_directory + '/dublin_core.xml')

    # dspace metadata schema
    root = ET.Element("dublin_core", schema='dspace')
    write_dspace = False
    for key in item.data:
        if key.startswith('dspace.'):
            if item.data[key]:
                elems = key.split('.')
                if len(elems) == 3:
                    ET.SubElement(root, "dcvalue", element=elems[1], qualifier=elems[2]).text = item.data[key]
                else:
                    ET.SubElement(root, "dcvalue", element=elems[1]).text = item.data[key]
                write_dspace = True
    if write_dspace:
        tree = ET.ElementTree(root)
        tree.write(saf_sub_directory + '/metadata_dspace.xml')

    # iiif metadata
    root = ET.Element("dublin_core", schema='iiif')
    write_iiif = False
    for key in item.data:
        if key.startswith('iiif.'):
            if item.data[key]:
                elems = key.split('.')
                if len(elems) == 3:
                    ET.SubElement(root, "dcvalue", element=elems[1], qualifier=elems[2]).text = item.data[key]
                else:
                    ET.SubElement(root, "dcvalue", element=elems[1]).text = item.data[key]
                write_iiif = True
    if write_iiif:
        tree = ET.ElementTree(root)
        tree.write(saf_sub_directory + '/metadata_iiif.xml')

    # local metadata
    root = ET.Element("dublin_core", schema='local')
    write_local = False
    for key in item.data:
        if key.startswith('local.'):
            if item.data[key]:
                elems = key.split('.')
                if len(elems) == 3:
                    ET.SubElement(root, "dcvalue", element=elems[1], qualifier=elems[2]).text = item.data[key]
                else:
                    ET.SubElement(root, "dcvalue", element=elems[1]).text = item.data[key]
                write_local = True
    if write_local:
        tree = ET.ElementTree(root)
        tree.write(saf_sub_directory + '/metadata_local.xml')


def check_extension(file):
    return file.lower().endswith(('.png', '.jpg', '.jpeg', '.jp2', '.j2k'))
