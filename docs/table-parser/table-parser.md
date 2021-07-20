---
layout: default
title: Table Parser
nav_order: 2
has_children: true
permalink: /table-parser
---

To overcome the issues of manually failed parsing, tables can now be imported from a TSV input; This is equivalent to copying and pasting a table from Excel into the curator HTML table input.

This allows the flexibility to edit an HTML(or PDF) table copied into Excel and then manually edited to conform to the requirements of the parser. There are some quirks and tricks to this so please report any common issues.

Importantly, this means you can delete one-line residues, split up multiple atom indices into multiple tables, or bread the "bad atom indices" into multiple rows.

__REQUIREMENTS:__

There are two possible TSV import formats:

- HTML-like TSV

This format requires ONE header row, but will still do the parsing of splitting chemical shifts, multiplicities, and J-coupling constants out of the table as it would do for a pure HTML table.

Here is an example TSV file which matches the required format. <a href="https://github.com/liningtonlab/npmrd_curator/raw/gh-pages/docs/assets/example_htmllike.tsv" download>HTML-like TSV</a>

- Manual TSV

This format allows a curator to manually input data from an old document that cannot be copy pasted.
The requirements for this input are much more stringent to simplify the parsing.
It requires ONE header row which _MUST_ match the specified headers of:

- `atom_index` _MUST_ be the first column and header
- `hshift` for proton chemical shifts - _MUST_ be a single decimal value
- `mult` for proton multiplicity
- `coup` for proton coupling constants - _MUST_ be a comma separate list of decimal values
- `cshift` for carbon-13 chemical shifts - _MUST_ be a single decimal value

You may have multiple compounds in a single table.

Here is an example TSV file which matches the required format. <a href="https://github.com/liningtonlab/npmrd_curator/raw/gh-pages/docs/assets/example_manual.tsv" download>Manual TSV</a>