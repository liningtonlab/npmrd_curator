# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:04:54 2020

@author: maras"""
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re
import csv
from collections import defaultdict

MULTI_REGEX = re.compile(
    r"(?:(?:hept|sept|sex|qui|s\s?br|(?!\whown)(?=\s)?\bs|\bt+d*|\bd+t*d*|\btt*|\bt|\bd|qd?|\bh|br\s?s|br\s?d+|br\s?t|br\s?q|m))+"
)

REGEX_V1 = re.compile(r"(?:(?:sept|s|d|t|q|h|br\s?s|br\s?d|br\s?t|br\s?q|m))+")


def input_str(input_str):
    """Takes str as input and returns BeautifulSoup object"""
    f = "".join([x.strip() for x in input_str.split("\n")])
    soup = BeautifulSoup(f.replace("&nbsp;", " ").replace("&nbsp", " "), "lxml")
    [soup.a.decompose() for i in soup.find_all("a")]
    return soup


def inputs(filepath):
    """Takes filepath as input and returns BeautifulSoup object"""
    inp_file1 = Path(filepath)  # UTF-8
    with inp_file1.open() as f:
        # minifies html
        f = "".join([x.strip() for x in f.read().split("\n")])
        # TODO: Ensure this is working properly to clear junk; check other parts that used I^ in search b/c now δ
        f = str(f).replace("&nbsp;", " ").replace("&nbsp", " ")
        if os.name == "nt":
            f = f.encode("cp1252")  # I don't understand, but this is required.
        # (Also must go from webpage html source code into new html file created in python)
        soup = BeautifulSoup(f, "lxml")
        [soup.a.decompose() for i in soup.find_all("a")]
    return soup


# Simple Functions
def num_columns(headers):
    ncol = len(headers)
    return ncol


def if_blank(i):
    if i == "":
        return True


def no_space_list(list):
    return [x for x in list if x != ""]


def no_space_2dlist(list_list):
    return [[x for x in list if x != ""] for list in list_list]


def cell_clean(i):
    """Takes string converting to text, removing line breaks/empty elements, strips extra whitespace"""
    return i.text.replace("\n", "").strip()


def all_same(items):
    """Takes list and checks if all the elements in said list are the same, returning True if so"""
    return all(map(lambda x: x == items[0], items))


def blanks_list(list_length):
    blanks = []
    for i in list_length:
        blanks1 = []
        for x in range(len(i)):
            blanks1.append(r"")
        blanks.append(blanks1)
    return blanks


# html Table Parsing Functions
def soup_id_headers(soup):
    """Takes soup object and returns column headers"""
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="colsep0 rowsep0")]
    return no_space_list(header_1)
    # TODO: See if way to include blanks; look at cell_clean


def soup_comp_id(soup):
    """Takes soup object and returns compound identification headers"""
    header_1 = [cell_clean(i) for i in soup.find_all("th", class_="rowsep1 colsep0")]
    return header_1


def create_new_td(soup):
    return soup.new_tag("td")


def soup_id_rows(soup):
    """Takes soup object and returns rows"""
    rows = soup.tbody.find_all("tr")
    clean_rows = []
    for idr, r in enumerate(rows):
        # want to use next n rows to fill in
        if any(x.get("rowspan") for x in r.find_all("td")):
            for idx, x in enumerate(r.find_all("td")):
                rs = int(x.get("rowspan", 0))
                if not rs:
                    continue
                for i in range(1, rs):
                    rn = rows[idr + i]
                    rn.insert(idx, create_new_td(soup))
        clean_rows.append([cell_clean(j) for j in r.find_all("td")])
    return clean_rows


def compound_number(compounds, headers):
    """Takes primary headers and compound id headers and returns the number of compounds.
    Based on len of compound id headers, numbers in main headers or number of hits of IH/IC"""

    comp_len = len(compounds)
    for i in headers:
        if re.compile(r"\d*[0-9]").search(i):
            header_len = len(headers) - 1
            if not comp_len:
                return header_len
            elif comp_len == header_len:
                return header_len
            elif comp_len != header_len:
                if header_len / 2 == comp_len:
                    return comp_len
                else:
                    return max(comp_len, header_len)
    if any(
        "δC" or "δH" in s for s in headers
    ):  # TODO: LOOK at and see if can add other cases(1st find diff pattern)
        search = ["δH", "δC"]
        result = {k: 0 for k in search}
        for item in headers:
            for search_item in search:
                if search_item in item:
                    result[search_item] += 1
        if result["δH"] == result["δC"]:
            return result.get("δH")
        else:
            return max(result.values())


def get_columns(rows, headers):
    """Takes rows and length of headers to get columns based on 2D list index from rows"""
    if headers:
        columns = [[x[j] for x in rows] for j in range(len(headers))]
        return columns
    else:
        raise Exception("Could not parse columns because of irregular headers")


def isListEmpty(inList):
    for item in inList:
        if item:
            return True
    return False


def atom_index_like(col):
    count = 0
    list_1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    list_1a = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a"]
    list_1b = ["1b", "2b", "3b", "4b", "5b", "6b", "7b", "8b", "9b"]
    for c in col:
        if c in list_1 or list_1a or list_1b:  # or list_1a or list_1b:
            count += 1
    return count > 4


def get_atom_index(columns, headers):
    if re.search(r"(position|^pos\.?|number|^no\.?|^[CH])", headers[0]):
        return columns[0], 0
    elif re.search(r"(^residue$|^amino\s?acid$|^unit(s)?$)", headers[0]):
        return columns[1], 1
    else:
        return None, None
    # elif atom_index_like(columns[0]):
    # headers[0] = "position"
    # print(atom_index_like(columns[0]))


def get_residues(columns, headers):
    if re.search(
        r"(^residue$|^amino\s?acid$|^unit(s)?$)", headers[0]
    ):  # Modify as example cases builds up
        residues = columns[0]
        return residues, 0
    else:
        return None, None


def is_2_d_nmr(headers):
    nmr2d_col_index = [
        idx
        for idx, i in enumerate(headers)
        if re.search(r"(HMBC)|(HSQC)|(([E]?CO|TOC|NOE|ROE)SY)", headers[idx])
    ]
    return nmr2d_col_index


def get_atom_index_column(columns):
    """Enumerate the list of columns so that positional index and atom_index can be returned"""
    return list(enumerate(columns))[0]
    # atom_index should be first column so can take that list and go from there


def is_float_test(value, list):
    try:
        val = float(value)
        list.append(val)
    except ValueError:
        pass


def str_list_average(input_list):
    """Takes a list of numerical strings and returns the average. Is able to ignore empty strings in list"""
    # vals = [float(i) for i in input_list if i]

    vals = []
    for i in input_list:
        if i:
            is_float_test(i, vals)
    return float("{:.2f}".format(sum(vals) / len(vals)))


def clean_cell_str(cell):
    # multiple types of dashes
    # cleanup dashes
    cell = re.sub(r"-|‒|–|—|―|⁓|−", "-", cell)
    # regularize and common typos
    return (
        cell.replace("..", ".")
        .replace(",", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace(";", "")
        .replace("/", " ")
        .strip()
    )


def all_blank(input_list):
    return all(x == "" for x in input_list)


def column_id_cleaner_list(columns, ignore_cols):
    """Takes 2dlist of columns . Searchs cells first for regex patterns to detect if column will contain H/C NMR, then each cell for regex patterns"""

    # Regex patterns; detect the table type to determine which column type
    ctype_pattern = re.compile(r"CH3|CH2|CH|q?C|NH2|NH|N[^D]|\bN$")
    coup_pattern = re.compile(r"\d+(?:\.\d+)?")

    # will be outputs
    H_spec = []
    Carbon_spec = []
    H_multiplicity = []
    J_coupling = []
    C_type = []
    for idc, col in enumerate(columns):
        if idc in ignore_cols:
            continue
        # Get all the chemical shifts first
        shifts = []
        for cell in col:
            # regularize strings
            cell = clean_cell_str(cell)
            # split on whitespace and get real strings
            cell_contents = [x for x in cell.split() if x]
            shift = ""
            if cell_contents:
                for idn, item in enumerate(cell_contents):
                    if re.search(coup_pattern, cell_contents[idn]):
                        shift = re.sub("[a-z]+$|^[a-z]+", "", cell_contents.pop(idn))
                        break

                # TODO: make case for: '213.0-123.0' or '2.23 - 22.123' then if '-0.13' or '- 0.13'
                # find ranges
                if re.search("\d+(?:\.\d+)\s?\-{1}\s?\d+(?:\.\d+)", shift):
                    shift.replace("-", "-")
                    shift = str_list_average(shift.split("-"))
                # if re.search("\−{1}\s?\d+(?:\.\d+)", shift):
                # shift.replace("-", "-")

                # if "-" in shift:
                #  shift = str_list_average(shift.split("-"))
                try:
                    shift = float(shift)
                except ValueError:
                    pass
            shifts.append(shift)

        avg = str_list_average(shifts)

        ctypes = []
        mults = []
        coups = []
        c_nmr = False
        h_nmr = False
        if 14.0 <= avg <= 250.0:
            c_nmr = True
            # for idx, cell in enumerate(col):
            # cell = clean_cell_str(cell.replace(str(shifts[idx]), ""))
            # ctype = ctype_pattern.findall(cell)
            # if ctype:
            #   ctypes.append(ctype[0])
            #  else:
            #   ctypes.append("")

        elif 0.0 <= avg <= 13.5:
            h_nmr = True
            for idx, cell in enumerate(col):
                cell_contents = [x for x in clean_cell_str(cell).split() if x]
                if cell_contents:
                    for idn, item in enumerate(cell_contents):
                        if re.search(coup_pattern, cell_contents[idn]):
                            cell_contents.pop(idn)
                            break

                    cell = " ".join(cell_contents)
                    # get multiplicity
                    mults.append("".join(MULTI_REGEX.findall(cell)))
                    # get j-couplings
                    coups.append(", ".join(coup_pattern.findall(cell)))
                else:
                    mults.append("")
                    coups.append("")

        else:
            print("WARNING - cannot handle this column")

        if c_nmr:
            Carbon_spec.append(shifts)
            # if not all_blank(ctypes):
            # C_type.append(ctypes)
        if h_nmr:
            H_spec.append(shifts)
            if not all_blank(mults):
                H_multiplicity.append(mults)
            if not all_blank(coups):
                J_coupling.append(coups)
    return H_spec, Carbon_spec, H_multiplicity, J_coupling, C_type


# def data_to_grid(numcomps, resi,  cspec, ctype, hspec, hmult, hcoup):
def data_to_grid(numcomps, aindex, **kwargs):
    if kwargs.get("resi"):
        headers = ["residues", "atom_index"]
        data = [kwargs.get("resi"), aindex]
    else:
        headers = ["atom_index"]
        data = [aindex]

    # Search for specified variables and create header and access dict
    possible_variables = {
        "cspec": "{0}_cspec",
        # "ctype": "{0}_ctype",
        "hspec": "{0}_hspec",
        "hmult": "{0}_multi",
        "hcoup": "{0}_coupling",
    }
    found_variables = {
        k: v
        for k, v in possible_variables.items()
        if k in kwargs.keys() and bool(kwargs.get(k))
    }
    hstring = ",".join(found_variables.values())
    for i in range(1, numcomps + 1):
        hl = hstring.format(i).split(",")
        headers.extend(hl)

    for j in range(numcomps):
        # data.extend([cspec[j], ctype[j], hspec[j], hmult[j], hcoup[j]])
        data.extend([kwargs.get(k)[j] for k in found_variables.keys()])
    return headers, data


def tableto_csv(headers, data, filename="html_parse_output.csv"):
    rows = zip(*data)
    with open(filename, "w", encoding="UTF-8", newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(headers)
        for row in rows:
            wr.writerow(row)


def get_float_avg(dict2):
    average_list = []
    cspec = []
    hspec = []

    for item in dict2:
        value_list = []
        for value in item:
            if type(value) == float:
                value_list.append(value)
        if not all_same(value_list):
            average = sum(value_list) / len(value_list)
            # average_list.append(average)
            if 14.0 <= average <= 250.0:
                cspec.append(list(item))
            elif 0.0 <= average <= 13.5:
                hspec.append(list(item))
    return cspec, hspec


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def fix_multidata(columns, ignore_cols):
    """Want to iterate over rows in columns and add rows when mulitdata present in at least one cell in a row.
    May require adding more than one cell?
    """
    # Step 1: detect when there are multidata cells
    rows_data_count = defaultdict(int)
    for idc, col in enumerate(columns):
        # skips aindex and residues
        if idc in ignore_cols:
            continue
        for row_idx, cell in enumerate(col):
            val_count = len(MULTI_REGEX.findall(cell))
            if val_count > rows_data_count[row_idx]:
                rows_data_count[row_idx] = val_count
    # Step 2: adds rows as required
    for row_idx in sorted(rows_data_count.keys(), reverse=True):
        count = rows_data_count[row_idx]
        if count > 1:
            # add count - 1 blank   rows
            for col in columns:
                for i in range(1, count):
                    col.insert(row_idx + i, "")
            # split data into them
            for col in columns:
                cell = clean_cell_str(col[row_idx])
                cell_contents = [x for x in cell.split() if x]
                if len(MULTI_REGEX.findall(" ".join(cell_contents))) > 1:
                    # print(" ".join(cell_contents))
                    data = []
                    for idc, _ in enumerate(cell_contents):
                        sub_cell = " ".join(cell_contents[idc:])
                        # this regex capture the following patterns -> groups
                        # '1.74 td' -> ('1.74 td', None)
                        # '1.74 td 1.67 m' -> ('1.74 td 1.67', ' 1.67')
                        # '1.74 td 13.8 3.5 1.67 m' -> ('1.74 td 13.8 3.5 1.67', ' 1.67')
                        # That is, it will only return a second group if there is a float following
                        # also, it will only capture the last trailing float, so it can be
                        # string subtracted from the right side of the string if there are more than 1 trailing floats
                        sub_match = re.search(
                            r"(^\d+(?:\.\d+) (?:(?:sept|s|d|t|q|h|br\s?s|br\s?d|br\s?t|br\s?q|m))+( ?\d+(?:\.\d+))*)",
                            sub_cell,
                        )
                        if sub_match:
                            g1, g2 = sub_match.groups()
                            if (
                                g2 and len(MULTI_REGEX.findall(sub_cell)) > 1
                            ):  # and there is a trailing multiplicty
                                # right hand string subtraction
                                g1 = "".join(g1.rsplit(g2, 1))
                            data.append(g1)
                    for idd, d in enumerate(data):
                        col[row_idx + idd] = d

