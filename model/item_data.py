from model.bitstream import Bitstream

# Static array of metadata field names used to validate and add fields.
item_data = [
    'Filename',
    'dc.title',
    'dc.description.abstract',
    'dc.description',
    'dc.contributor.author',
    'dc.contributor',
    'dc.date.issued',
    'dc.date.created',
    'dc.subject',
    'dc.publisher',
    'dc.type',
    'dc.coverage.spatial',
    'dc.rights',
    'dc.rights.uri',
    'dc.format.medium',
    'dc.format.extent',
    'dspace.iiif.enabled',
    'iiif.canvas.naming'
]


class Item:
    """
    A class to populate a dictionary with keys based on dspace dublin core field names.
    """

    # Class data dictionary of metadata values
    data = {'dc.title': None,
            'dc.description.abstract': None,
            'dc.description': None,
            'dc.contributor.author': None,
            'dc.contributor': None,
            'dc.date.issued': None,
            'dc.date.created': None,
            'dc.subject': None,
            'dc.publisher': None,
            'dc.type': None,
            'dc.coverage.spatial': None,
            'dc.rights': None,
            'dc.rights.uri': None,
            'dc.format.medium': None,
            'dc.format.extent': None,
            'dspace.iiif.enabled': None,
            'iiif.canvas.naming': None,
            'bitstreams': []
            }

    def __init__(self):
        """
        Initialize the Item with the default dictionary.
        """
        self.reset()

    def set_value(self, key: str, value: str):
        """
        Set a value for a specific key in the dictionary.

        :param key: The key to update.
        :param value: The value to set for the key.
        :raises
        Raises: ValueError: If the key is not a valid dublin core field.

        :return: void
        """

        # Verify the key is part of the static array of metadata fields.
        if key not in item_data:
            raise ValueError(f"Invalid key '{key}'.")

        self.data[key] = value

    def get_value(self, key: str):
        """
        Get the value for a specific key from the dictionary.

        :param key: The key to retrieve.
        :raises: ValueError: If the key is not one a valid dublin core field name.
        :return: The value associated with the key.
        """
        if key not in self.data:
            raise ValueError(f"Invalid key '{key}'.")

        return self.data[key]

    def add_bitstream(self, bitstream: Bitstream):
        """
        Add copy of the bitstream object to bitstream list
        :param bitstream:
        :return:
        """
        self.data['bitstreams'].append(bitstream.bitstream_data.copy())

    def reset(self):
        """
        Reset the dictionary to its initial state with all keys set to None.
        """
        for key in self.data.keys():
            if key == 'bitstreams':
                self.data[key] = []
            else:
                self.data[key] = None

    def __str__(self):
        """
        Return a string representation of the dictionary.
        """
        return str(self.data)
