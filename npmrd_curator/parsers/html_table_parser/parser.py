from bs4 import BeautifulSoup
import re
from typing import List, Tuple, Union, Optional
from collections import defaultdict

from npmrd_curator.parsers.html_table_parser import utils


MULTI_REGEX = re.compile(
    r"(?:(?:hept|sept|sex|qui|s\s?br|(?!\whown)(?=\s)?\bs|\bt+d*|\bd+t*d*|\btt*|\bt|\bd|qd?|\bh|br\s?s|br\s?d+|br\s?t|br\s?q|m))+"
)


def read_html(input_str: str) -> BeautifulSoup:
    """Takes str, does cleaning as input and returns BeautifulSoup object"""
    f = utils.clean_input(input_str)
    soup = BeautifulSoup(f, "lxml")
    # removes all anchor elements/links and contents thereof
    [a.decompose() for a in soup.find_all("a")]
    return soup


def find_headers(soup: BeautifulSoup) -> List[str]:
    """Takes soup object and returns column headers"""
    header_rows = soup.find("thead").find_all("tr")
    return [utils.cell_clean(i) for i in header_rows[-1].find_all("th")]


def find_rows(soup: BeautifulSoup) -> List[List[str]]:
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
                    rn.insert(idx, utils.create_new_td(soup))
        clean_rows.append([utils.cell_clean(j) for j in r.find_all("td")])
    return clean_rows


def get_columns(rows: List[List[str]]) -> List[List[str]]:
    """Takes data rows and converts to columns"""
    return [[x[j] for x in rows] for j in range(len(rows[0]))]


def is_atom_index_like(col: List[str]) -> bool:
    count = 0
    idx_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    idx_regexp = re.compile("^(" + "|".join([f"{i}(a|b)?" for i in idx_list]) + ")$")
    for c in col:
        if idx_regexp.match(c):
            count += 1
    return count > 4


def is_atom_index_header(head: str) -> Optional[re.Match]:
    return re.search(r"(position|^pos\.?|number|^no\.?|^[CH])", head)


def is_residue_header(head: str) -> Optional[re.Match]:
    return re.search(r"(^residue$|^amino\s?acid$|^unit(s)?$)", head)


def get_atom_index(
    columns: List[List[str]], headers: List[str]
) -> Union[Tuple[List[str], int], Tuple[None, None]]:
    """Looks at headers and tries to find atom indices.
    Failing this it looks for atom index-like columns.

    TODO: perhaps refactor for multiple indices
    """
    acceptable_column_range = [0, 1]
    # look at headers first
    for idx in acceptable_column_range:
        if is_atom_index_header(headers[idx]):
            return columns[idx], idx
    # look at columns second
    for idx in acceptable_column_range:
        if is_atom_index_like(columns[idx]):
            return columns[idx], idx
    return None, None


def get_residues(
    columns: List[List[str]], headers: List[str]
) -> Union[Tuple[List[str], int], Tuple[None, None]]:
    """Look at headers and detect resides/subunits columns"""
    if is_residue_header(headers[0]):
        return columns[0], 0
    return None, None


def get_2dnmr_indices(headers: List[str]) -> List[int]:
    """Examine headers for 2D NMR signatures and return column indices"""
    nmr2d_col_index = [
        idx
        for idx, i in enumerate(headers)
        if re.search(r"(HMBC)|(HSQC)|(([E]?CO|TOC|NOE|ROE)SY)", headers[idx])
    ]
    return nmr2d_col_index


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
                cell = utils.clean_cell_str(col[row_idx])
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


def column_resolve(columns: List[List[str]], ignore_cols: List[int]):
    """Takes 2dlist of columns . Searchs cells first for regex patterns
    to detect if column will contain H/C NMR, then each cell for regex patterns
    """

    # Regex patterns; detect the table type to determine which column type
    # ctype_pattern = re.compile(r"CH3|CH2|CH|q?C|NH2|NH|N[^D]|\bN$")
    coup_pattern = re.compile(r"\d+(?:\.\d+)?")

    # will be outputs
    H_spec = []
    Carbon_spec = []
    H_multiplicity = []
    J_coupling = []
    # C_type = []
    for idc, col in enumerate(columns):
        if idc in ignore_cols:
            continue
        # Get all the chemical shifts first
        shifts = []
        for cell in col:
            # regularize strings
            cell = utils.clean_cell_str(cell)
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
                    shift = utils.str_list_average(shift.split("-"))
                # if re.search("\−{1}\s?\d+(?:\.\d+)", shift):
                # shift.replace("-", "-")

                # if "-" in shift:
                #  shift = str_list_average(shift.split("-"))
                try:
                    shift = float(shift)
                except ValueError:
                    pass
            shifts.append(shift)

        avg = utils.str_list_average(shifts)

        # ctypes = []
        mults = []
        coups = []
        c_nmr = False
        h_nmr = False
        if 14.0 <= avg <= 250.0:
            c_nmr = True

        elif 0.0 <= avg <= 13.5:
            h_nmr = True
            for idx, cell in enumerate(col):
                cell_contents = [x for x in utils.clean_cell_str(cell).split() if x]
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
        if h_nmr:
            H_spec.append(shifts)
            if not utils.all_blank(mults):
                H_multiplicity.append(mults)
            if not utils.all_blank(coups):
                J_coupling.append(coups)
    # return H_spec, Carbon_spec, H_multiplicity, J_coupling, -
    return H_spec, Carbon_spec, H_multiplicity, J_coupling


def data_to_grid(aindex, **kwargs):
    if kwargs.get("resi"):
        headers = ["residues", "atom_index"]
        data = [kwargs.get("resi"), aindex]
    else:
        headers = ["atom_index"]
        data = [aindex]

    # Search for specified variables and create header and access dict
    possible_variables = {
        "cspec": "{0}_cspec",
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

    compound_count = 1
    while True:
        hl = hstring.format(compound_count).split(",")
        headers.extend(hl)
        try:
            # data.extend([cspec[j], ctype[j], hspec[j], hmult[j], hcoup[j]])
            data.extend(
                [kwargs.get(k)[compound_count - 1] for k in found_variables.keys()]
            )
            compound_count += 1
        except IndexError:
            break

    return headers, data, compound_count