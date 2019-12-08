
def get_frequencies(names_data_generator):
    freq_dict = {}
    for name_data in names_data_generator:
        name = name_data["name"]
        frequency = len(name_data["titles"])
        freq_dict[name] = frequency

    return freq_dict
