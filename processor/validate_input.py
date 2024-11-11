import os

from model.item_data import item_data


def validate(input_values: list, directory: str):
    print('Broken file names:\n')
    for index, row in enumerate(input_values):
        file = row['Filename']
        if file is None:
            print('Empty file name column at index: ' + str(index))
        if not os.path.exists(directory + '/' + file):
            print(file)

    print('\n')

    print("Invalid input fields fields:\n")
    for key in input_values[0].keys():
        if key not in item_data:
            print('Invalid key: ' + key)

    print('\n')
