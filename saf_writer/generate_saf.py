import os
import shutil
import xml.etree.cElementTree as ET
from pathlib import Path
from zipfile import ZipFile

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
    nested_directory_path = Path(saf_directory, 'saf_import_files_unzipped', f"{count:04}")
    nested_directory_path.mkdir(parents=True, exist_ok=True)

    saf_sub_directory = os.path.join(saf_directory, 'saf_import_files_unzipped',  f"{count:04}")

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

    archive = saf_directory + '/saf_output.zip'

    file_paths = get_all_file_paths(saf_directory)

    with ZipFile(archive, 'w') as zipper:
        # writing each file one by one
        for file in file_paths:
            p = Path(file).parts
            arcname = os.path.join('saf-import', p[-2], p[-1])
            zipper.write(file, arcname)


def check_extension(file):
    return file.lower().endswith(('.png', '.jpg', '.jpeg', '.jp2', '.j2k'))


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        if 'saf_import_files_unzipped' in root:
            for filename in files:
                # join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

    # returning all file paths
    return file_paths


def make_directory(directory):
    try:
        os.mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")