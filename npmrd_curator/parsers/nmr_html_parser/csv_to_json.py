import csv
import json
from pathlib import Path

# CSV reformatting to structure for JSON


def no_blank(input_string):
    if input_string == "":
        return False
    else:
        return True


def input_file(filepath):
    # CSV input to csv.DictReader to get dictionary
    inp_file_path = Path(filepath)
    with open(inp_file_path, encoding="UTF-8") as csvFile:
        return list(csv.DictReader(csvFile))


def csv_dict_reader_extraction(input_list):
    # Cleans up csv.DictReader, sorting columns as values with key as column header
    new_dict = {}
    for d in input_list:
        for k, v in d.items():
            if k in new_dict:
                new_dict[k] = new_dict[k] + [v]
            else:
                new_dict[k] = [v]
    return new_dict


def dictionary_parser(num_comps, csv_dict):
    # Sorts data and separates out for each compound
    comps_shift_data = {}
    for i in range(1, num_comps + 1):
        possible_variables = [
            str(i) + "_cspec",
            str(i) + "_hspec",
            str(i) + "_multi",
            str(i) + "_coupling",
        ]
        found_variables = {
            key: val
            for key, val in csv_dict.items()
            if key in possible_variables and bool(csv_dict.get(key))
        }
        comps_shift_data["compound_" + str(i)] = found_variables
    return comps_shift_data


def c_nmr_shift_creator(shifts_list, atom_input_list):
    # Collects cnmr data together into a dictionary for each atom
    return [
        ({"rdkit_index": None, "shift": float(shift), "atom_index": atom})
        for shift, atom in zip(shifts_list, atom_input_list)
        if no_blank(shift)
    ]


def coupling_float(coup):
    try:
        if no_blank(coup):
            return [float(coup)]
    except ValueError:
        coup_list = [float(x.strip()) for x in coup.split(",")]
        return coup_list


def multi_blank(multi):
    if no_blank(multi):
        return multi
    else:
        pass


def h_nmr_shift_multi_coup_creator(shifts_list, atom_input_list, multi_list, coup_list):
    # Collects hnmr data together into a dictionary for each atom

    data = [
        {
            "rdkit_index": None,
            "shift": float(shift),
            "atom_index": atom,
            "multiplicity": multi_blank(multi),
            "coupling": coupling_float(coup),
        }
        for shift, atom, multi, coup in zip(
            shifts_list, atom_input_list, multi_list, coup_list
        )
        if no_blank(shift)
    ]
    # return data

    for i, val in enumerate(data):
        if not val["atom_index"]:
            data[i]["atom_index"] = data[i - 1]["atom_index"]
    return data
    # TODO: Work with residue table types, not sure about
    # if new_dict["residues"]:
    # else: new_dict["atom_index"]
    # print(shift_creator(shift_comps["compound_"+str(index+1)][str(index+1)+"_cspec"], new_dict["atom_index"]))


def json_structuring(comps_data, csv_dict):
    # New Nested template dictionary for each compound, that becomes list of dictionaries in the end
    # Requires formatting data into JSON output
    list_comp_dictionary = []
    # iterating over each compound
    for index, (kk, vv) in enumerate(comps_data.items()):
        comp_dictionary = {
            "name": None,
            "smiles": None,
            "origin_doi": None,
            "origin_type": None,
            "origin_genus": None,
            "origin_species": None,
            "c_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": c_nmr_shift_creator(
                    comps_data["compound_" + str(index + 1)][str(index + 1) + "_cspec"],
                    csv_dict["atom_index"],
                ),
            },
            "h_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": h_nmr_shift_multi_coup_creator(
                    comps_data["compound_" + str(index + 1)][str(index + 1) + "_hspec"],
                    csv_dict["atom_index"],
                    comps_data["compound_" + str(index + 1)][str(index + 1) + "_multi"],
                    comps_data["compound_" + str(index + 1)][
                        str(index + 1) + "_coupling"
                    ],
                ),
            },
        }
        list_comp_dictionary.append(comp_dictionary)
    return list_comp_dictionary


def json_dump(data, filename):
    # Writing to JSON file
    with open(filename, "w") as f:
        # json.dump(data, f)
        # nicer output
        f.write(json.dumps(data, indent=2))  # indent=2 instead of just f.
