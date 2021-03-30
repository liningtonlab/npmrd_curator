"""
Takes TSV input from npmrd_curator app in one of two forms.
1. HTML copy pasted into Excel and then copy pasted into the webform.
2. Manually entered values in Excel.

In both cases, the inputs should be square grids (i.e. no merged cells)

In both cases there should be EXACTLY one header column, but in different formats:

1. Data names from HTML table. If there is more than one header column, 
    delete unneeded ones.
2. Each compound MUST have the following headers for every or no compounds:
    a. 1H NMR - hshift, mult, coup
    b. 13C NMR - cshift
"""
import pandas as pd
