"""Takes data blocks and converts to ACS style guide string.
"""
from typing import Dict
from statistics import mean


def write_all(data: Dict) -> str:
    n = data.get("name", "")
    # add space to name if present
    if n:
        n = f"{n} "
    optr = optical_rotation(data.get("optical_rotation"))
    uv = uv_spectroscopy(data.get("uv_spectroscopy"))
    ir = ir_spectroscopy(data.get("ir_spectroscopy"))
    cnmr = c_nmr(data.get("c_nmr"))
    hnmr = h_nmr(data.get("h_nmr"))

    return f"{n+' ' if n else ''}{'; '.join(filter(bool, [optr, uv, ir, cnmr, hnmr]))}"


def optical_rotation(data: Dict) -> str:
    if not data:
        return ""
    t = data["temperature"]
    r = data["reference"]
    v = data["value"]
    sign = "+" if v > 0 else ""  # Sign include - when neg and + when pos
    c = data["concentration"]
    s = data["solvent"]
    return f"[α]{t}{r} {sign}{v} (c {c:.02f}, {s})"


def uv_spectroscopy(data: Dict) -> str:
    if not data:
        return ""
    spec = ", ".join(
        [
            f"{s[0]} ({s[1]})"
            for s in map(
                lambda x: (x["wavelength"], x["absorptivity"]), data["spectrum"]
            )
        ]
    )
    s = data["solvent"]
    u = data["units"]
    is_log = mean([x["absorptivity"] for x in data["spectrum"]]) < 10
    return f"UV ({s}) λmax, {u} ({'log ' if is_log else ''}ε) {spec}"


def ir_spectroscopy(data: Dict) -> str:
    if not data:
        return ""
    s = data["solvent"]
    u = data["units"]
    spec = ", ".join(map(str, data["spectrum"]))
    return f"IR ({s}) (cm-1) {spec}"


def _cnmr_shift(x: Dict) -> str:
    return f"{float(x['shift'])}"


def c_nmr(data: Dict) -> str:
    if not data:
        return ""
    f = data["frequency"]
    s = data["solvent"]
    a = data["ambiguous"]
    ambi = ""
    if a:
        ambi = ", " + ", ".join(a)
    spec = ", ".join(map(_cnmr_shift, data["spectrum"]))
    return f"13C NMR ({f'{f}, ' if f else ''}{s}, δ): {spec}{ambi}"


def _hnmr_shift(x: Dict) -> str:
    # "2.79 (dt, J = 5.5, 9.7 Hz, 1H)"
    s = float(x["shift"])
    j = x["coupling"]
    i = x["integration"]
    j_str = ""
    if j:
        j_str = f"J = {', '.join(map(str, j))} Hz, "
    m = x["multiplicity"]
    return f"{s:.02f} ({m}, {j_str}{i}H)"


def h_nmr(data: Dict) -> str:
    if not data:
        return ""
    f = data["frequency"]
    s = data["solvent"]
    a = data["ambiguous"]
    ambi = ""
    if a:
        ambi = ", " + ", ".join(a)
    spec = ", ".join(map(_hnmr_shift, data["spectrum"]))
    return f"1H NMR ({f'{f}, ' if f else ''}{s}, δ): {spec}{ambi}"
