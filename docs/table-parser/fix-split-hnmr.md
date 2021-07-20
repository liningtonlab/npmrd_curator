---
layout: default
title: Split 1H NMR Data
parent: Table Parser
nav_order: 1
---

# Solving Split 1H HMR data in the TSV parser

Jeffrey van Santen – 21/3/2021

In the article [https://www.nature.com/articles/ja2016161](https://www.nature.com/articles/ja2016161) there is an NMR data table with each data type in separate columns.

![split table](/npmrd_curator/assets/images/split_hnmr_table.png)

While you could use the "Manual TSV" method, there is an easier solution which requires a little bit of Excel-fu.

I will show you an example of fixing this using the `TEXTJOIN` function in Excel instead. The below example concatenates the above table to just **Compound 1.**

**First** – copy+paste the table into Excel with only a single header row.

![split table solo](/npmrd_curator/assets/images/split_table_solo.png)

**Second** – In a new column, use the `TEXTJOIN` Excel function to join all the 1H NMR data into a single string (`=TEXTJOIN(" ", TRUE, D2:F2)` in the below case).

![split table text join](/npmrd_curator/assets/images/split_table_solo_textjoin.png)

Then copy and paste this for all rows in the table.

![split table copy paste](/npmrd_curator/assets/images/split_table_solo_cp.png)

You then want to clean up this table to the correct format. In this case I removed the C-multiplicity column and moved the new 1H data column (by copying and selecting "PASTE VALUE" in Excel) next to the 13C data column (with an appropriate header). The result should look as follows 

![split table clean](/npmrd_curator/assets/images/split_table_solo_clean.png)

You can then copy and paste this table in the npmrd\_curator app and should see a successful parsing:

![split table success](/npmrd_curator/assets/images/split_table_solo_success.png)