import copy
import csv
import re
from pathlib import Path
from typing import Dict, List, Union, Optional
from itertools import zip_longest

# CSV reformatting to structure for JSON


def no_blank(input_string: Optional[str]) -> bool:
    """Checks whether a string is blank"""
    return input_string != "" and input_string is not None


def coupling_float(coup: str) -> List[float]:
    coup_list = []
    try:
        if no_blank(coup):
            coup_list = [float(coup)]
    except ValueError:
        coup_list = [float(x.strip()) for x in coup.split(",")]
    return coup_list


def multi_blank(multi: str) -> Optional[str]:
    if no_blank(multi):
        return multi
    return None


def load_csv(filepath: Union[Path, str]) -> List[Dict]:
    """CSV input to csv.DictReader to get dictionary"""
    inp_file_path = Path(filepath)
    with open(inp_file_path, encoding="UTF-8") as csvFile:
        return list(csv.DictReader(csvFile))


def listdict_to_dictlist(listdict: List[Dict]) -> Dict[str, List]:
    """Cleans up csv.DictReader, sorting columns as values with key as column header"""
    new_dict: Dict[str, List] = {}
    for d in listdict:
        for k, v in d.items():
            k = k.strip()
            v = v.strip()
            if k in new_dict:
                new_dict[k] = new_dict[k] + [v]
            else:
                new_dict[k] = [v]
    return new_dict


def column_dict_parser(num_comps: int, csv_dict: Dict) -> Dict:
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


def c_nmr_factory(shifts: List, atom_indices: List):
    # Collects cnmr data together into a dictionary for each atom
    return [
        ({"rdkit_index": None, "shift": float(shift), "atom_index": atom})
        for shift, atom in zip(shifts, atom_indices)
        if no_blank(shift)
    ]


def h_nmr_factory(
    atom_index: List[str],
    lit_atom_index: List[str],
    shifts_list: List[str],
    multi_list: List[str],
    coup_list: List[str],
):
    # Collects hnmr data together into a dictionary for each atom
    # TODO: Work with residue table types
    data: List[Dict] = [
        {
            "shift": float(shift),
            "multiplicity": multi_blank(multi),
            "coupling": coupling_float(coup),
            "lit_atom_index": laidx,
            "atom_index": aidx,
            "rdkit_index": [],
            "interchangable_index": [],
        }
        for aidx, laidx, shift, multi, coup in zip_longest(
            atom_index, lit_atom_index, shifts_list, multi_list, coup_list
        )
        if no_blank(shift)
    ]

    return data


def json_structuring(comps_data: Dict, csv_dict: Dict):
    # New Nested template dictionary for each compound, that becomes list of dictionaries in the end
    # Requires formatting data into JSON output
    output = []
    # CNMR doesn't need lit atom indices because they don't get modified
    # Only HNR indices get modified
    for idx in comps_data.keys():
        comp = {
            "name": None,
            "np_mrd_id": None,
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
                "spectrum": c_nmr_factory(
                    comps_data.get(idx, {}).get(f"{idx}_cshift", []),
                    csv_dict["atom_index"],
                ),
            },
            "h_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": h_nmr_factory(
                    csv_dict["atom_index"],
                    csv_dict["lit_atom_index"],
                    comps_data.get(idx, {}).get(f"{idx}_hshift", []),
                    comps_data.get(idx, {}).get(f"{idx}_multi", []),
                    comps_data.get(idx, {}).get(f"{idx}_coupling", []),
                ),
            },
        }
        output.append(comp)
    return output


def merge_atom_indices(inp_dict: Dict) -> Dict:
    """Problem consecutive rows with different atom indices relating to same
    carbon atom index
    """
    csv_dict = copy.deepcopy(inp_dict)
    # safety check, i would never expect this to happen
    aidx = csv_dict.get("atom_index")
    if not aidx:
        print("WARNING - no atom index!")
        return csv_dict
    # Add copy of original atom_indices to dict
    csv_dict["lit_atom_index"] = copy.deepcopy(aidx)
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
            last_idx_int = int(re.match(r"\d+", last_idx).group())  # type: ignore
            this_idx_int = int(re.match(r"\d+", aidx[i]).group())  # type: ignore
        except (TypeError, AttributeError):
            continue
        if last_idx_int != this_idx_int:
            continue
        # test for 13C in this row - don't merge if so
        for k in filter(lambda x: "cshift" in x, csv_dict.keys()):
            v = csv_dict[k]
            # If there are any values in carbon spec for this row, then don't merge
            if not v[i]:
                aidx[i] = last_idx
    return csv_dict
