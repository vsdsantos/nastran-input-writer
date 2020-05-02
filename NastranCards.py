# -*- coding: utf-8 -*-
"""
Created on Sun May 12 14:47:52 2019

@author: Victor
"""

import NastranInput as nst


# AEFACT (SID, D1, D2, ...)
def write_aefact(SID: int, *args) -> [str]:
    return nst.dynamic_field_writer('AEFACT', [2], [SID], nst.REAL, *args)


# PAERO5 (PID, NALPHA, LALPHA, NXIS, LXIS, NTAUS, LTAUS, CAOC1, CAOC2, CAOC3, CAOC4, CAOC5, ...)
def write_paero5(pid: int, nalpha: int, lalpha: int, nxis: int, lxis: int, ntaus: int, ltaus: int, *args) -> [str]:
    form = [2, 2, 2, 2, 2, 2, 2, 0]  # PAERO5, PID, NALPHA, LALPHA, NXIS, LXIS, NTAUS, LTAUS, , ,
    data = [pid, nalpha, lalpha, nxis, lxis, ntaus, ltaus, '']
    return nst.dynamic_field_writer('PAERO5', form, data, nst.REAL, *args)
    # form_2 = [-1,1,1,1,1,0,0,0,0,0] # , CAOC1, CAOC2, CAOC3, CAOC4
    # line_2 = nst.small_field_format_line(form_2, ['']+list(args[6:])+['', '', '', '', ''])
    # return [line_1, line_2]


# MKAERO1 ([m1, m2, ...], [k1, k2, k3, ...])
def write_mkaero1(machs: [], red_freqs: []) -> [str]:
    form_1 = [3] + [1 for _ in range(len(machs))] + [0 for _ in range(8 - len(machs))] + [-1]  # MKAERO1, m1, m2, ...
    form_2 = [-1] + [1 for _ in range(len(red_freqs))] + [0 for _ in range(8 - len(red_freqs))] + [0]  # , k1, k2, ...
    line_1 = nst.small_field_format_line(form_1, ['MKAERO1'] + machs + ['' for _ in range(8 - len(machs))] + [''])
    line_2 = nst.small_field_format_line(form_2, [''] + red_freqs + ['' for _ in range(8 - len(red_freqs))] + [''])
    return [line_1, line_2]


# CAERO5 (EID, PID, CP, NSPAN, LSPAN, NTHRY, NTHICK, X1, Y1, Z1, X12, X4, Y4, Z4, X43)
def write_caero5(EID: int, PID: int, *args) -> [str]:
    form_1 = [3, 2, 2, 2, 2, 0, 2, 2, 0, -1]  # CAERO5, EID, PID, CP, NSPAN, LSPAN, NTHRY, NTHICK, , ,
    form_2 = [-1, 1, 1, 1, 1, 1, 1, 1, 1, 0]  # , X1, Y1, Z1, X12, X4, Y4, Z4, X43
    line_1 = nst.small_field_format_line(form_1, ['CAERO5', EID, PID] + list(args[0:5]) + ['', ''])
    line_2 = nst.small_field_format_line(form_2, [''] + list(args[5:]) + [''])
    return [line_1, line_2]


# SPLINE1 (EID, CAERO, BOX1, BOX2, SETG, DZ, METH, USAGE, NELEM?, MELEM?)
def write_spline1(EID: int, *args) -> [str]:
    result = []

    if len(args) == 9:
        form_1 = [3, 2, 2, 2, 2, 2, 1, 3, 3, -1]  # SPLINE2, EID, CAERO, BOX1, BOX2, SETG, DZ, METH, USAGE, ,
        form_2 = [-1, 1, 1, 0, 0, 0, 0, 0, 0, 0]  # , NELEM, MELEM
    else:
        form_1 = [3, 2, 2, 2, 2, 2, 1, 3, 3, 0]  # SPLINE2, EID, CAERO, BOX1, BOX2, SETG, DZ, METH, USAGE, ,
        form_2 = []

    data_1 = ['SPLINE1', EID] + list(args[:7]) + ['']
    line_1 = nst.small_field_format_line(form_1, data_1)
    result.append(line_1)
    if len(args) == 9:
        data_2 = [''] + list(args[7:9]) + [''] + list(args[9:]) + ['', '', '', '', '']
        line_2 = nst.small_field_format_line(form_2, data_2)
        result.append(line_2)
    return result


# SPLINE2 (EID, CAERO, ID1, ID2, SETG, DZ, DTOR, CID, DTHX, DTHY, USAGE)
def write_spline2(EID: int, *args) -> [str]:
    form_1 = [3, 2, 2, 2, 2, 2, 1, 1, 2, -1]  # SPLINE2, EID, CAERO, ID1, ID2, SETG, DZ, DTOR, CID, ,
    form_2 = [-1, 1, 1, 0, 3, 0, 0, 0, 0, 0]  # , DTHX, DTHY, , USAGE
    data_1 = ['SPLINE2', EID] + list(args[:7]) + ['']
    data_2 = [''] + list(args[7:9]) + [''] + list(args[9:]) + ['', '', '', '', '']
    line_1 = nst.small_field_format_line(form_1, data_1)
    line_2 = nst.small_field_format_line(form_2, data_2)
    return [line_1, line_2]


def write_aero(*args) -> [str]:
    form = [3, 2, 2, 1, 1, 0, 0, 0, 0, 0]
    return [nst.small_field_format_line(form, ['AERO'] + list(args) + ['', '', '', '', ''])]


def write_flutter(*args) -> [str]:
    form = [3, 2, 3, 2, 2, 2, 0, 2, 0, 0]
    return [nst.small_field_format_line(form, ['FLUTTER'] + list(args[:-1]) + ['', args[-1]])]


def write_param(data_type: int, name: str, value) -> [str]:
    form = [3, 3, data_type, 0, 0, 0, 0, 0, 0, 0]
    return [nst.small_field_format_line(form, ['PARAM', name, value] + ['' for _ in range(7)])]


def write_flfact(ID: int, *args) -> [str]:
    return nst.dynamic_field_writer('FLFACT', [2], [ID], nst.REAL, *args)


def write_eigr(low_freq, high_freq, n_modes) -> [str]:
    form_1 = [3, 2, 3, 1, 1, 0, 2, 0, 0, -1]
    form_2 = [-1, 3, 0, 0, 0, 0, 0, 0, 0, 0]
    line_1 = nst.small_field_format_line(form_1, ['EIGR', 20, 'AGIV', low_freq, high_freq, '', n_modes, '', '', ''])
    line_2 = nst.small_field_format_line(form_2, ['', 'MAX'] + ['' for _ in range(8)])
    return [line_1, line_2]

