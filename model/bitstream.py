
class Bitstream:

    bitstream_labels = ['iiif.label', 'iiif.toc', 'iiif.description', 'Filename']

    bitstream_data = {
        'Filename': None,
        'iiif.label': None,
        'iiif.description': None,
        'iiif.toc': None
    }

    def __init__(self):
        """
        Initialize the Bitstream with the default dictionary.
        """
        self.reset()

    def set_value(self, key: str, value: str):
        """
        Set a value for a specific key in the dictionary.

        :param key: The key to update.
        :param value: The value to set for the key.
        :raises: ValueError: If the key is not a valid field.
        :return:
        """

        if key not in self.bitstream_data:
            raise ValueError(f"Invalid key '{key}'.")

        self.bitstream_data[key] = value

    def get_value(self, key: str):
        """
        Get the value for a specific key from the dictionary.

        :param key: The key to retrieve.
        :raises: ValueError: If the key is not one a valid field name.
        :return: The value associated with the key.
        """

        if key not in self.bitstream_data:
            raise ValueError(f"Invalid key '{key}'.")

        return self.bitstream_data[key]

    def reset(self):
        """
        Reset the dictionary to its initial state with all keys set to None.
        """
        for key in self.bitstream_data.keys():
            self.bitstream_data[key] = None
