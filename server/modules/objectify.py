import json


def make_object_array(list_of_tuples):
    """ Converts a list of tuples to a JSON array of objects. """

    object_list = []

    for tuple in list_of_tuples:
        word = tuple[0]
        frequency = tuple[1]

        # Store word-frequency pair in a Python dictionary
        pair = {
            'text': word,
            'value': frequency
        }

        # Add this dictionary to the list
        object_list.append(pair)

    # Convert the list into a JSON array
    return json.dumps(object_list)
