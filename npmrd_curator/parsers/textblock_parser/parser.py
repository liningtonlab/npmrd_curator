import json
import re


def data_split(text):
    split_patterns = re.split(";|\.\s", text)
    return split_patterns


def rotation_tag(text):
    rotation_data = []
    for data_block in text:
        rotation_patterns = ["[α]", "α"]
        for pattern in rotation_patterns:
            if pattern in data_block:
                rotation_data.append(data_block)
    return rotation_data


def rotation_parsing(text):
    rotation = {
        "temperature": None,
        "reference": None,
        "value": None,
        "concentration": None,
        "solvent": None,
    }
    temperature = None
    reference = None
    value = None
    concentration = None
    solvent = None
    join = "".join(text)
    temperature_pattern1 = "(α.*)(\d+)(D)"
    temperature_pattern2 = "(\s)(\d+)(\s°C)"
    temperature_pattern3 = "(α.*D\s)(\d+)"
    temperature_pattern4 = "(α.*)(\d+)(\s)(D)"
    temperature_pattern = [
        temperature_pattern1,
        temperature_pattern2,
        temperature_pattern3,
        temperature_pattern4,
    ]
    for patterns in temperature_pattern:
        temperature = re.search(patterns, join)
        if temperature:
            catch_temperature = temperature.group(2)
            rotation["temperature"] = float(catch_temperature)
    reference_pattern = re.search("(D)", join)
    if reference_pattern:
        catch_reference = reference_pattern.group(1)
        rotation["reference"] = catch_reference
    value_pattern1 = "(\–)(\d+.\d+)"
    value_pattern2 = "(\−)(\d+.\d+)"
    value_pattern3 = "(\+)(\d+.\d+)"
    value_pattern4 = "(\-)(\d+.\d+)"
    value_pattern5 = "(\−)(\d+)"
    value_pattern = [
        value_pattern1,
        value_pattern2,
        value_pattern3,
        value_pattern4,
        value_pattern5,
    ]
    for patterns in value_pattern:
        value = re.search(patterns, join)
        if value:
            catch_value = value.group(2)
            rotation["value"] = float(catch_value)
    concentration_pattern1 = "(c\s)(\d+.\d+)"
    concentration_pattern2 = "(c\s=\s)(\d+.\d+)"
    concentration_pattern3 = "(\d+.\d+)(\sg\/\d+\smL)"
    concentration_pattern = [
        concentration_pattern1,
        concentration_pattern2,
        concentration_pattern3,
    ]
    for patterns in concentration_pattern:
        concentration = re.search(patterns, join)
        if concentration and patterns != concentration_pattern3:
            catch_concentration = concentration.group(2)
            rotation["concentration"] = float(catch_concentration)
        if concentration and patterns == concentration_pattern3:
            catch_concentration = concentration.group(1)
            rotation["concentration"] = float(catch_concentration)
    solvent_patterns1 = "(\,\s)(\w+)(\))"
    solvent_patterns2 = "(in\s)(\w+)"
    solvent_pattern = [solvent_patterns1, solvent_patterns2]
    for patterns in solvent_pattern:
        solvent = re.search(patterns, join)
        if solvent:
            catch_solvent = solvent.group(2)
            rotation["solvent"] = catch_solvent
    return rotation


def ir_match_tag(text):
    """Detect IR data from splitted spectral sample text.
    param text:splitted spectral sample text
    return:string related to IR data
    """
    match = [data_types for data_types in text if "IR" in data_types]
    return match


def ir_parsing(text):
    """Parsing IR data to detect solvent,units and spectrum values.
   param text:IR data block
   return:a dictionary that include all the information about solvent, units and IR spectrum values
   """
    IR_Spectroscopy = {"solvent": None, "units": None, "spectrum": {}}
    spectrum_values = []
    join = "".join(text)
    split = join.replace(",", "").split(" ")
    # Extract numbers from list of string
    for value in split:
        try:
            val = int(value)
            spectrum_values.append(val)
        except ValueError:
            try:
                val = float(value)
                spectrum_values.append(val)
            except ValueError:
                continue
    # Find solvent,unit,spectrum data and add them into a dictionary
    solvent_pattern1 = "(\()(\w*)(\))"
    solvent_pattern2 = "(\()(\w*)"
    pattern = [solvent_pattern1, solvent_pattern2]
    for value in split:
        for patterns in pattern:
            solvent_match = re.search(patterns, value)
            if solvent_match:
                catch_solvent = solvent_match.group(2)
                IR_Spectroscopy["solvent"] = catch_solvent
            unit_match = re.search(r"(cm..)", value)
            if unit_match:
                catch_unit = unit_match.group(1)
                IR_Spectroscopy["units"] = catch_unit
    IR_Spectroscopy["spectrum"] = spectrum_values
    return IR_Spectroscopy


def uv_match_tag(text):
    """Detect UV data from splitted spectral sample text.
    param text:splitted spectral sample text
    return:string related to UV data
    """
    match = [data_block for data_block in text if "UV" in data_block]
    return match


def uv_parsing(text):
    """Parsing UV data to detect solvent ,units and spectrum values.
    param text:UV data block
    return:a dictionary that include all the information about solvent, units and UV spectrum values
    """
    UV_spectroscopy = {"solvent": None, "units": None, "spectrum": []}
    spectrum_vals = []
    join = "".join(text)
    solvent_match = re.search(r"(\()(\w+)(\))", join)
    solvent = None
    units = None
    if solvent_match:
        catch_solvent = solvent_match.group(2)
        solvent = catch_solvent
    unit_match = re.search(r"(nm)", join)
    if unit_match:
        catch_unit = unit_match.group(2)
        units = catch_unit
    UV_spectroscopy["solvent"] = solvent
    UV_spectroscopy["units"] = units
    spectrum_values = re.search(u"(\(log ε\)) (.*)", join)
    if spectrum_values:
        catch_values = spectrum_values.group(2)
        split = catch_values.split(",")
        for idx, item in enumerate(split):
            wavelength = None
            absorptivity = None
            wavelength_values = re.findall(
                r"(?<![\d.])[0-9]+(?![\d.])", item
            )  # Extract wavelength values
            if wavelength_values:
                val = "".join(wavelength_values)
                wavelength = int(val)
            absorption_values = re.findall(r"\((\d+.\d+)\)", item)
            if absorption_values:
                val = "".join(absorption_values)
                absorptivity = float(val)
            spectrum_vals.append(
                {"wavelength": wavelength, "absorptivity": absorptivity}
            )
    UV_spectroscopy["spectrum"] = spectrum_vals
    return UV_spectroscopy


def cnmr_match_tag(text):
    """Detect Carbon NMR data from splitted spectral sample text
    param text:splitted spectral sample text
    return:string related to Carbon NMR data
    """
    cnmr_data = []
    for data_block in text:
        cnmr_patterns = ["13C NMR", "13C{1H}"]
        for pattern in cnmr_patterns:
            if pattern in data_block:
                cnmr_data.append(data_block)
    return cnmr_data


def cnmr_parsing(text):
    """Parsing Carbon NMR data to detect solvent,temperature,reference,frequency and spectrum values.
    param text:Carbon NMR data block
    return:a dictionary that include all the information about solvent,temperature,reference,frequency and Carbon NMR
    spectrum values
    """
    ambiguous_vals = []
    spec_values = []
    CNMR_spectroscopy = {
        "solvent": None,
        "temperature": None,
        "reference": None,
        "frequency": None,
        "spectrum": None,
        "ambiguous": None,
    }
    join = "".join(text)
    freq_pattern1 = "(\d* MHz)"
    freq_pattern2 = "(\d+.\d+ MHz)"
    freq_patterns = [freq_pattern1, freq_pattern2]
    for items in freq_patterns:
        frequency = re.search(items, join)
        if frequency:
            catch_freq = frequency.group(1)
            CNMR_spectroscopy["frequency"] = catch_freq
    # Different patterns to detect solvent with different textual format
    pattern1 = "(NMR\s\()(\w*...)(\,\s\d*\sMHz\))"
    pattern2 = "(NMR\s\(\d*\sMHz\,\s)(\w*)(\))"
    pattern3 = "(NMR\s\()(\w*)(\))"
    pattern4 = "(NMR\s\(\d+.\d+\sMHz\,\s)(\w*)(\))"  # ex: NMR (62.5 MHz, CDCl3)
    pattern5 = "(NMR\s\(\d+\sMHz\,\s\d+\sK\,\s)(\w+)(\))"  # ex: 1 H NMR (400 MHz, 298 K, CDCl3)
    pattern6 = "(NMR\s\(\d*\sMHz\,\s)(\w*\-\w*)(\))"
    pattern7 = "(NMR\s\(\d*\sMHz\,\s)(\w*\-\w*\d*)(\))"
    pattern8 = "(NMR\s\(\d+\sMHz\,\s)(\w*)(\,\s\w*\))"
    pattern9 = "(NMR\s\δ\s\(\d+\sMHz\,\s)(\w*)(\,\s\w*\))"
    pattern10 = "(NMR\s\(\d*\sMHz\,\s)(\w*\-\w*\d*)(\,\s\w+\s\w+\s\w+\))"  # 13C NMR (151 MHz, DMSO-d6, mix of rotamers)
    pattern = [
        pattern1,
        pattern2,
        pattern3,
        pattern4,
        pattern5,
        pattern6,
        pattern7,
        pattern8,
        pattern9,
        pattern10,
    ]
    for patterns in pattern:
        match = re.search(patterns, join)
        if match:
            solvent = match.group(2)
            CNMR_spectroscopy["solvent"] = solvent
        else:
            continue
    shift_pattern1 = "(?<=\)).*$"
    shift_patterns = [shift_pattern1]
    for patterns in shift_patterns:
        match_specval = re.findall(patterns, join)  # Extract spectrum data after δ sign
        if match_specval:
            print(match_specval)
            join2 = "".join(match_specval)
            typeA_pattern = re.search(
                "\d+.\d+\-\d+.\d+\s\(.*\,\s.*\)", join2
            )  # Detect following example pattern
            # ex: 1.33–1.22 (22H, m)
            typeB_pattern1 = "(\d+.\d+)(\s\(.*\,\s.*\))"
            typeB_pattern2 = "(^\d+)(\s\(.*\,\s.*\))"
            typeB_all = [typeB_pattern1, typeB_pattern2]
            typeC_pattern = re.search("", join2)
            for patterns in typeB_all:

                typeB_pattern = re.search(patterns, join2)
                if typeB_pattern:
                    print("typeB")
                    chunks = re.split("(?<=\))", join2)
                    for idx, item in enumerate(chunks):
                        shift = None
                        atom_index = None
                        rdkit_index = None
                        result = re.search(patterns, item)
                        if result:
                            catch_typeB = result.group(1)
                            shift = float(catch_typeB)
                            # spec_values.append(
                            #   {
                            #      "shift": shift,
                            #      "atom_index": atom_index,
                            #      "rdkit_index": rdkit_index,
                            # }
                            # )
            # CNMR_spectroscopy["spectrum"] = spec_values
            if typeA_pattern:
                print("typeA")
                chunks = re.split(
                    "(?<=\))", join2
                )  # Spectrum data extracted after δ sign,splitted after "\)"parentheses
                clean_chunks = [x.strip(",") for x in chunks]
                str_list = [x for x in clean_chunks if x != "" and x != "."]
                ambiguous_vals.append(str_list)
                CNMR_spectroscopy["ambiguous"] = ambiguous_vals
            else:

                # split = re.split('\;|\,', join2)
                split = join2.split(",")
                for idx, item in enumerate(split):
                    shift = None
                    atom_index = None
                    rdkit_index = None
                    match1 = re.search("(\d+.\d+\–\d+.\d+\s\(.*\))", item)
                    # match5 = re.search("(\d+.\d+\s\–\s\d+.\d+\s\(.*\))", item)
                    match2 = re.search(
                        "(\d+.\d+)(\s\(.*\))", item
                    )  # Detect following example pattern,ex: 206.1 (C3)
                    match3 = re.search(
                        "(\d+.\d+)(\(.*\)\s\(.*\))", item
                    )  # 129.4(0) (Ar), 129.3(8) (Ar)
                    match4 = re.search(
                        "(\d+.\d+)(\(.*\))", item
                    )  # ex :78.4(9), 78.4(6)

                    if match1:
                        typeA_pattern = match1.group(1)
                        ambiguous_vals.append(typeA_pattern)
                    # if not match1 and match5:
                    #   pattern = match5.group(1)
                    # print(typeA_pattern)
                    # ambiguous_vals.append(pattern)
                    elif not match1 and not match3 and match2:
                        typeA_pattern = match2.group(1)
                        # print(typeA_pattern)
                        shift = float(typeA_pattern)
                        # spec_values.append({"shift": shift, "atom_index": atom_index, "rdkit_index": rdkit_index})
                    elif not match1 and not match2 and match3:
                        pattern = match3.group(1)
                        # print(pattern)
                        shift = float(pattern)
                    elif not match1 and not match2 and not match3 and match4:
                        pattern = match4.group(1)
                        # print(pattern)
                        shift = float(pattern)
                    else:
                        try:
                            val = int(item)
                            shift = val
                        except ValueError:
                            try:
                                val = float(item)
                                shift = val
                            except ValueError:
                                try:
                                    val = str(item)
                                    findfloat = re.findall("(\d+.\d+)", val)
                                    join = "".join(findfloat)
                                    finalval = float(join)
                                    shift = finalval
                                except ValueError:
                                    continue
                    spec_values.append(
                        {
                            "shift": shift,
                            # "atom_index": atom_index,
                            # "rdkit_index": rdkit_index,
                        }
                    )
                CNMR_spectroscopy["ambiguous"] = ambiguous_vals
                CNMR_spectroscopy["spectrum"] = spec_values
    return CNMR_spectroscopy


def hnmr_match_tag(text):
    """Detect H NMR data from splitted spectral sample text.
    param text:splitted spectral sample text
    return:string related to H NMR data
    """
    hnmr_data = []
    for data_block in text:
        hnmr_patterns = ["1H NMR", "1 H NMR", "1HNMR"]
        for pattern in hnmr_patterns:
            if pattern in data_block:
                hnmr_data.append(data_block)
    return hnmr_data


def hnmr_data(text):
    join = "".join(text)
    match_specval = re.findall("(?<=\)\sδ).*$", join)
    match_specval3 = re.findall("(?<=\(ppm\)).*$", join)
    match_specval4 = re.findall("(?<=δH\)).*$", join)
    match_specval5 = re.findall(
        "(?<=\)).*$", join
    )  # ex:1H NMR δ (600 MHz, CDCl3, Me4Si) 7.38 – 7.18
    match_specval6 = re.findall("(?<=1 H NMR\sδ).*$", join)
    match_specval7 = re.findall("(?<=1H NMR\:).*$", join)
    # match_specval8 = re.findall("(?<=1H NMR\sδ).*$", join)
    if match_specval:
        match_specval2 = re.findall("(?<=δ).*$", join)
        join2 = "".join(match_specval2)
        chunks = re.split("(?<=\))", join2)
        clean_chunks = [x.strip(",") for x in chunks]
        str_list = [x for x in clean_chunks if x != ""]
        return str_list
    if match_specval3:
        join3 = "".join(match_specval3)
        chunks = re.split("(?<=\))", join3)
        clean_chunks = [x.strip(",") for x in chunks]
        str_list = [x for x in clean_chunks if x != ""]
        return str_list
    if match_specval4:
        join4 = "".join(match_specval4)
        chunks = re.split("(?<=\))", join4)
        clean_chunks = [x.strip(",") for x in chunks]
        str_list = [x for x in clean_chunks if x != ""]
        return str_list
    if match_specval6:
        join5 = "".join(match_specval6)
        chunks = re.split("(?<=\))", join5)
        clean_chunks = [x.strip(",") for x in chunks]
        str_list = [x for x in clean_chunks if x != ""]
        return str_list
    if match_specval7:
        join7 = "".join(match_specval7)
        chunks = re.split("(?<=\))", join7)
        clean_chunks = [x.strip(",") for x in chunks]
        str_list = [x for x in clean_chunks if x != ""]
        return str_list
    # if match_specval8:
    #   join8 = "".join(match_specval8)
    #  chunks = re.split("(?<=\))", join8)
    # clean_chunks = [x.strip(",") for x in chunks]
    # str_list = [x for x in clean_chunks if x != ""]
    # return str_list
    else:
        join6 = "".join(match_specval5)
        chunks = re.split("(?<=\))", join6)
        clean_chunks = [x.strip(",") for x in chunks]
        str_list = [x for x in clean_chunks if x != ""]
        return str_list


def hnmr_parsing(hnmr_list, data_list):
    nmr_values = {
        "solvent": None,
        "temperature": None,
        "reference": None,
        "frequency": None,
        "spectrum": None,
        "ambiguous": None,
    }
    spectrum_vals = []
    ambiguous_vals = []
    integration_pattern1 = (
        "(\()(\d+)(\w+\,)"  # ex: 4.93 (1H, dd, J = 8.9, 4.0 Hz, H-29)
    )
    integration_pattern2 = "(\,\s)(\d+)(\w+\))"  # ex: 3.4 (d, J = 2.6 Hz, 1H)
    integration_pattern3 = "(\,\s)(\d+)(\w+\,)"  # ex: 7.43 (d, J = 8.1 Hz, 4H, Ar−H)
    integration_pattern4 = "(\,\s)(\d+)(\s\w+\))"  # ex: δ 2.87 (d, J = 4.8 Hz, 3 H)
    integration_pattern5 = "(\,)(\d+)(\s\w+\))"  # ex: 7.16 (t, J = 8.1 Hz,1 H)
    integration_pattern6 = "(\,\s)(\d+)(\s\w+\,)"  # (m, 2 H, Ar)
    integration_pattern7 = "(\,\s)(\d+.\d+)(\s\w+\))"  # ex :(br, 0.03 H)
    integration_pattern8 = "(\,\s)(\d+.\d+)(\sH\,)"  # ex:(d, 0.05 H, J = 5.3 Hz, H-1e)
    integration_patterns = [
        integration_pattern1,
        integration_pattern2,
        integration_pattern3,
        integration_pattern4,
        integration_pattern5,
        integration_pattern6,
        integration_pattern7,
        integration_pattern8,
    ]
    pattern_list = [
        "s",
        "d",
        "q",
        "t",
        "dd",
        "br",
        "m",
        "dq",
        "dt",
        "ddd",
        "dtt",
        "tq",
        "bd",
        "bs",
        "br s",
        "br d",
        "sept",
        "septet",
        "sextet",
        "sext",
        "brs",
        "s br",
        "app dq",
        "app ddt",
        "app q",
    ]
    multiplicity_pattern1 = "(\()(\D+)(\,)"  # ex: 7.93 (d, J = 2.6 Hz, 1H)
    multiplicity_pattern2 = (
        "(\,\s)(\D+)(\,)"  # ex: 4.93 (1H, dd, J = 8.9, 4.0 Hz, H-29)
    )
    multiplicity_pattern3 = "(\,\s)(\D+)(\))"  # ex: 3.72 (3H, s)
    multiplicity_patterns = [
        multiplicity_pattern1,
        multiplicity_pattern2,
        multiplicity_pattern3,
    ]
    solvent = (None,)
    temperature = None
    reference = None
    frequency = None
    join = "".join(hnmr_match_tag(data_list))
    freq_pattern = re.search(r"(\d*\sMHz)", join)
    if freq_pattern:
        freq_catch = freq_pattern.group(1)
        frequency = freq_catch
    pattern1 = "(NMR\s\()(\w*...)(\,\s\d*\sMHz\))"
    pattern2 = "(NMR\s\(\d*\sMHz\,\s)(\w*)(\))"
    pattern3 = "(NMR\s\(\d*\sMHz\,\s)(\w*\-\w*)(\))"
    pattern4 = "(NMR\s\()(\w*)(\))"
    pattern5 = "(NMR\s\(\d+.\d+\sMHz\,\s)(\w*)(\))"  # ex: NMR (62.5 MHz, CDCl3)
    pattern6 = "(NMR\s\(\d+\sMHz\,\s\d+\sK\,\s)(\w+)(\))"
    pattern7 = "(NMR\s\(\d*\sMHz\,\s)(\w*\-\w*\d*)(\))"
    pattern8 = "(NMR\s\(\d+\sMHz\,\s)(\w*)(\,\s\w*\))"
    pattern9 = "(NMR\s\δ\s\(\d+\sMHz\,\s)(\w*)(\,\s\w*\))"  # ex: 1H NMR δ (600 MHz, CDCl3, Me4Si)
    pattern10 = "(NMR\s\(\d*\sMHz\,\s)(\w*\-\w*\d*)(\,\s\w+\s\w+\s\w+\))"
    pattern = [
        pattern1,
        pattern2,
        pattern3,
        pattern4,
        pattern5,
        pattern6,
        pattern7,
        pattern8,
        pattern9,
        pattern10,
    ]
    for patterns in pattern:
        solvent_match = re.search(patterns, join)
        if solvent_match:
            solvent_catch = solvent_match.group(2)
            solvent = solvent_catch
        else:
            continue
    nmr_values["solvent"] = solvent
    nmr_values["temperature"] = temperature
    nmr_values["reference"] = reference
    nmr_values["frequency"] = frequency
    for idx, item in enumerate(hnmr_list):
        shift = None
        integration = None
        multiplicity = None
        coupling = []
        atom_index = None
        rdkit_index = None

        shift_match1 = re.search("(\d+.\d+)(\s\(.*\))", item)
        shift_match2 = re.search("(\d+.\d+\-\d+.\d+\s\(.*\))", item)
        shift_match3 = re.search("(\d+.\d+\–\d+.\d+\s\(.*\))", item)
        shift_match4 = re.search("(\d+.\d+\s\–\s\d+.\d+\s\(.*\))", item)
        shift_match5 = re.search("(\d+.\d+\−\d+.\d+\s\(.*\))", item)
        if (
            shift_match1
            and not shift_match2
            and not shift_match3
            and not shift_match4
            and not shift_match5
        ):
            shift_valueoriginal = shift_match1.group(
                1
            )  # ex: 8.73 (d, J = 8.8 Hz, 1H), # ex: 7.37-7.33 (m, 3H)
            shift = float(shift_valueoriginal)

        elif shift_match1 and shift_match3:
            shift_value = shift_match3.group(1)
            ambiguous_vals.append(shift_value)
            continue

        elif shift_match1 and shift_match2:
            shift_value = shift_match2.group(1)
            ambiguous_vals.append(shift_value)
            continue

        elif shift_match1 and shift_match4:
            shift_value = shift_match4.group(1)
            ambiguous_vals.append(shift_value)
            continue

        elif shift_match1 and shift_match5:
            shift_value = shift_match5.group(1)
            ambiguous_vals.append(shift_value)
            continue
        else:
            continue

        for patterns in integration_patterns:
            match = re.search(patterns, item)
            if (
                match
                and not shift_match2
                and not shift_match3
                and not shift_match4
                and not shift_match5
            ):
                integration_value = match.group(2)
                val = float(integration_value)
                integration = val
            else:
                continue

        for patterns in multiplicity_patterns:
            match = re.search(patterns, item)
            if (
                match
                and not shift_match2
                and not shift_match3
                and not shift_match4
                and not shift_match5
            ):
                multiplicity_value = match.group(2)
                if multiplicity_value in pattern_list:
                    multiplicity = multiplicity_value
                else:
                    continue
            else:
                continue
        coupling_match1 = re.findall("J\s=\s(.*)\sHz", item)
        if (
            coupling_match1
            and not shift_match2
            and not shift_match3
            and not shift_match4
            and not shift_match5
        ):
            join = "".join(coupling_match1)
            # print(join)
            split = join.split(",")
            # print(split)
            coupling = [float(i) for i in split]
        if (
            not coupling_match1
            and not shift_match2
            and not shift_match3
            and not shift_match4
            and not shift_match5
        ):
            coupling_match2 = re.findall("J\s=\s(.*)\,", item)
            if coupling_match2:
                join = "".join(coupling_match2)
                split = join.split(",")
                # print(split)
                coupling = [float(i) for i in split]
        spectrum_vals.append(
            {
                "shift": shift,
                "integration": integration,
                "multiplicity": multiplicity,
                "coupling": coupling,
                # "atom_index": atom_index,
                # "rdkit_index": rdkit_index,
            }
        )
    nmr_values["ambiguous"] = ambiguous_vals
    nmr_values["spectrum"] = spectrum_vals
    return nmr_values


def parse_text(text, output_file=None):
    data_list = data_split(text)
    # rotation_match = rotation_tag(data_list)
    # IR_match = ir_match_tag(data_list)
    # UV_match = uv_match_tag(data_list)
    CNMR_match = cnmr_match_tag(data_list)
    HNMR_match = hnmr_match_tag(data_list)
    hnmrdata_blocks = hnmr_data(HNMR_match)
    data = {
        "name": None,
        "np_mrd_id": None,
        "smiles": None,
        "original_isolation": False,
        "origin_doi": None,
        "origin_type": None,
        "origin_genus": None,
        "origin_species": None,
        # "optical_rotation": rotation_parsing(rotation_match),
        # "ir_spectroscopy": ir_parsing(IR_match),
        # "uv_spectroscopy": uv_parsing(UV_match),
        "c_nmr": cnmr_parsing(CNMR_match),
        "h_nmr": hnmr_parsing(hnmrdata_blocks, data_list),
    }
    if output_file:
        with open(output_file, "w") as fd:
            fd.write(json.dumps(indent=2,))
    return data
