import copy
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Union

# CSV reformatting to structure for JSON


def no_blank(input_string: str) -> bool:
    """Checks whether a string is blank"""
    return input_string != ""


def load_csv(filepath: Union[Path, str]) -> List[Dict]:
    """CSV input to csv.DictReader to get dictionary"""
    inp_file_path = Path(filepath)
    with open(inp_file_path, encoding="UTF-8") as csvFile:
        return list(csv.DictReader(csvFile))


def csv_dict_reader_extraction(input_list):
    """Cleans up csv.DictReader, sorting columns as values with key as column header"""
    new_dict = {}
    for d in input_list:
        for k, v in d.items():
            if k in new_dict:
                new_dict[k] = new_dict[k] + [v]
            else:
                new_dict[k] = [v]
    return new_dict


def dictionary_parser(num_comps: int, csv_dict: Dict) -> Dict:
    """Sorts data and separates out for each compound"""
    comps_shift_data = {}
    for i in range(1, num_comps + 1):
        # Creates list of possible variables for a compound
        possible_variables = [
            str(i) + "_cshift",
            str(i) + "_hshift",
            str(i) + "_multi",
            str(i) + "_coupling",
        ]
        # Find the variables for a single compound
        # from the input data
        found_variables = {
            key: val
            for key, val in csv_dict.items()
            if key in possible_variables and bool(csv_dict.get(key))
        }
        comps_shift_data[str(i)] = found_variables
    return comps_shift_data


def c_nmr_shift_creator(shifts_list, atom_input_list):
    # Collects cnmr data together into a dictionary for each atom
    return [
        ({"rdkit_index": None, "shift": float(shift), "atom_index": atom})
        for shift, atom in zip(shifts_list, atom_input_list)
        if no_blank(shift)
    ]


def coupling_float(coup):
    coup_list = []
    try:
        if no_blank(coup):
            coup_list = [float(coup)]
    except ValueError:
        coup_list = [float(x.strip()) for x in coup.split(",")]
    return coup_list


def multi_blank(multi):
    if no_blank(multi):
        return multi


def h_nmr_shift_multi_coup_creator(
    atom_index, lit_atom_index, shifts_list, multi_list, coup_list
):
    # Collects hnmr data together into a dictionary for each atom
    # TODO: Work with residue table types
    data = [
        {
            "shift": float(shift),
            "multiplicity": multi_blank(multi),
            "coupling": coupling_float(coup),
            "lit_atom_index": laidx,
            "atom_index": aidx,
            "rdkit_index": [],
            "interchangable_index": [],
        }
        for aidx, laidx, shift, multi, coup in zip(
            atom_index, lit_atom_index, shifts_list, multi_list, coup_list
        )
        if no_blank(shift)
    ]

    return data


def json_structuring(comps_data, csv_dict):
    # New Nested template dictionary for each compound, that becomes list of dictionaries in the end
    # Requires formatting data into JSON output
    list_comp_dictionary = []
    # iterating over each compound
    # for index, (kk, vv) in enumerate(comps_data.items()):
    for idx in comps_data.keys():
        comp_dictionary = {
            "name": None,
            "smiles": None,
            "original_isolation": False,
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
                    comps_data.get(idx, {}).get(f"{idx}_cshift", []),
                    csv_dict["atom_index"],
                ),
            },
            "h_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": h_nmr_shift_multi_coup_creator(
                    csv_dict["atom_index"],
                    csv_dict["lit_atom_index"],
                    comps_data.get(idx, {}).get(f"{idx}_hshift", []),
                    comps_data.get(idx, {}).get(f"{idx}_multi", []),
                    comps_data.get(idx, {}).get(f"{idx}_coupling", []),
                ),
            },
        }
        list_comp_dictionary.append(comp_dictionary)
    return list_comp_dictionary


def merge_atom_indices(csv_dict):
    """Problem consecutive rows with different atom indices relating to same
    carbon atom index
    """
    # safety check, i would never expect this to happen
    aidx = csv_dict.get("atom_index")
    # Add copy of original atom_indices to dict
    csv_dict["lit_atom_index"] = copy.deepcopy(aidx)
    if not aidx:
        print("WARNING - no atom index!")
        return
    # Check for any atom indices with look like 1a/1b or 1alpha/1beta
    # Using regex to parse int
    for i, val in enumerate(aidx):
        # skips the first one or any ominous other bugs
        try:
            last_idx = aidx[i - 1]
        except IndexError:
            continue
        # Replace atom index blank with previous
        if not val:
            aidx[i] = last_idx
            csv_dict["lit_atom_index"][i] = last_idx
        # Check for same int value as previous
        # Also need to make sure relevant
        # this usually indicates attachement to another group
        if "-" in val:
            continue
        try:
            last_idx_int = int(re.match(r"\d+", last_idx).group())
            this_idx_int = int(re.match(r"\d+", aidx[i]).group())
        except (TypeError, AttributeError):
            continue
        if last_idx_int != this_idx_int:
            continue
        # relevance here = testing for 13C in this row
        for k in filter(lambda x: "cshift" in x, csv_dict.keys()):
            v = csv_dict[k]
            # If there are any values in carbon spec for this row, then don't merge
            if not v[i]:
                aidx[i] = last_idx
