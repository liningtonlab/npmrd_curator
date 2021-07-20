---
layout: default
title: Changelog
nav_order: 3
--- 

## Changelog

##### 2021-04-23

- Automatically remove integration values from cells
- Fix case sensitivity in atom_index header name detection

##### 2021-04-21

- Removed HTML from Table parser branding 
- Fixed bug preventing correct parsing of 1H NMR data from Manual TSV
- Fixed bug preventing correct parsing of 1H NMR data when not all three types of shift, multiplicity, and coupling.

##### 2021-03-31

- Add ability to import tables from TSV (copy paste from Excel) in two formats:

1. A table which was copy pasted from an HTML / PDF.

![submit tsv1](/assets/images/submit_tsv1.png)

2. A table which was manually entered into excel. This REQUIRES specific headers.

![submit tsv2](/assets/images/submit_tsv2.png)

See the [TSV Tables Section](#1.1-tsv-tables) for full details on requirements.

- Add error handling to report to users on table parsing failures.

##### 2021-01-25

- Add ability to save current state of curator app to JSON. (*NOTE* this is intended to begin the ability to import state). 

![save state](/assets/images/save_state.png)


##### 2021-01-13

- Fixed a bug related to resetting atom indices (it previously did not work properly for a mixed set of text blocks and tables)
- Fixed a bug related to selection of protons by selecting the core C or heteroatom
- Added the ability to change the SMILES of a compound on the atom remapping page. This will also automatically reset the atom map selection.

![change smiles](/assets/images/change_smiles.gif)

- Added the ability to remove a compound from the final dataset.

![remove compound](/assets/images/remove_compound.gif)
