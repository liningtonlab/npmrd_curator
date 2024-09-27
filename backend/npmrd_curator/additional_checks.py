import copy

def check_if_data_has_index_assignments(data):
    """
    checks if "rdkit_index" exists in spectrum data of h_nmr or c_nmr and sets "has_index_assignments"
    to True, if they do, False if they do not, and None if there aren't any shift values.

    Args:
        data (dict): The "data" entry to check for assignments
    """
    try:
        data_copy = copy.deepcopy(data)
        for compound_entry in data:
            if len(compound_entry['h_nmr']['spectrum']) > 0:
                if "rdkit_index" in compound_entry.get('h_nmr', {}).get('spectrum', [{}])[0]:
                    compound_entry['h_nmr']['has_index_assignments'] = True
                else:
                    compound_entry['h_nmr']['has_index_assignments'] = False
            else:
                compound_entry['h_nmr']['has_index_assignments'] = None

            if len(compound_entry['c_nmr']['spectrum']) > 0:
                if "rdkit_index" in compound_entry.get('c_nmr', {}).get('spectrum', [{}])[0]:
                    compound_entry['c_nmr']['has_index_assignments'] = True
                else:
                    compound_entry['c_nmr']['has_index_assignments'] = False
            else:
                compound_entry['c_nmr']['has_index_assignments'] = None
        
        return data_copy
    except:
        return data
        
    