from model.bitstream import Bitstream


class Item:
    """
    A class to populate a dictionary with keys based on dspace dublin core field names.
    """

    # Class variable to store the dictionary
    data = {'dc.title': None,
            'dc.description.abstract': None,
            'dc.description': None,
            'dc.contributor.author': None,
            'dc.contributor': None,
            'dc.date.issued': None,
            'dc.date.created': None,
            'dc.subject': None,
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

    def set_value(self, key, value):
        """
        Set a value for a specific key in the dictionary.

        Args:
        key (str): The key to update.
        value: The value to set for the key.

        Raises:
        ValueError: If the key is not a valid dublin core field.
        """
        if key not in self.data:
            raise ValueError(f"Invalid key '{key}'.")

        self.data[key] = value

    def get_value(self, key):
        """
        Get the value for a specific key from the dictionary.

        Args:
        key (str): The key to retrieve.

        Returns:
        The value associated with the key.

        Raises:
        ValueError: If the key is not one a valid dublin core field name.
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


