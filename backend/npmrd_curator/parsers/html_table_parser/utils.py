from typing import List
from bs4 import BeautifulSoup, Tag
import re
import numpy as np


def clean_input(input_str: str) -> str:
    f = minify(input_str)
    for schar in ["&nbsp;", "&nbsp"]:
        f = f.replace(schar, " ")
    return f


def minify(input_str: str) -> str:
    return "".join([x.strip() for x in input_str.split("\n")])


def cell_clean(cell):
    return cell.text.replace("\n", "").strip()


def remove_blanks(lst: List[str]) -> List[str]:
    return [x for x in lst if x != ""]


def create_new_td(soup: BeautifulSoup) -> Tag:
    return soup.new_tag("td")


def all_blank(input_list):
    return all(x == "" for x in input_list)


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def str_list_average(input_list):
    """Takes a list of numerical strings and returns the average. Is able to ignore empty strings in list"""
    # vals = [float(i) for i in input_list if i]
    # avoid long repeated decimals with format_float_scientific
    return float(
        np.format_float_scientific(
            np.fromiter(filter(is_float, input_list), dtype=np.float64).mean(),
            precision=4,
        )
    )


def remove_integration(s: str) -> str:
    """Search for integration values in cell and strip them"""
    return re.sub(r"(1|2|3)H,\s?", "", s)


def clean_cell_str(cell):
    # multiple types of dashes
    # cleanup dashes
    cell = re.sub(r"-|‒|–|—|―|⁓|−", "-", cell)
    # remove integration values
    cell = remove_integration(cell)
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