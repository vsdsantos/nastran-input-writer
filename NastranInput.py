# -*- coding: utf-8 -*-
"""
Created on Sat May 11 14:20:33 2019

@author: Victor Santos
"""
import math
import copy

CONTINUE = -1
EMPTY = 0
REAL = 1
INTEGER = 2
LITERAL = 3

SMALL_FIELD_SIZE = 8
LARGE_FIELD_SIZE = 16


# form = [LITERAL, REAL, REAL, INTEGER, REAL, REAL, REAL, REAL, REAL, INTEGER]
# data = ['CRO', 0.1122, -14.99999999, 0, 24, 5432.54, 0.3333, 1e-99, -90.9, 100]

def format_integer(data, size, tab):
    return ' {:{tab}{size}d}'.format(data, size=size - 1, tab=tab)


def format_real(data, size, tab):
    if data == 0:
        return '{:{tab}{size}}'.format('0.0', size=size, tab=tab)
    integer_part = math.floor(data) if data > 0 else math.ceil(data)
    if integer_part == 0 or data > 10 ** (size - 3) - 0.1:
        sz = size - 7 if data > 0 else size - 8
        return ' {:{tab}.{size}E}'.format(data, size=sz, tab=tab)
    else:
        integer_size = len('{:}'.format(integer_part))
        decimal_size = size - integer_size - 2
        return ' {:{tab}.{size}f}'.format(data, size=decimal_size, tab=tab)


def format_literal(data, size, tab):
    return '{:{tab}{size}}'.format(data, size=size, tab=tab)


def format_data_point(data_point_form, field_size, tab, point):
    if data_point_form == REAL:
        return format_real(point, field_size, tab)
    elif data_point_form == INTEGER:
        return format_integer(point, field_size, tab)
    elif data_point_form == LITERAL:
        return format_literal(point, field_size, tab)
    elif data_point_form == EMPTY:
        return format_literal('', field_size, tab)
    elif data_point_form == CONTINUE:
        return format_literal('+', field_size, tab)


def small_field_format_line(data_format, data):
    line = format_data_point(data_format[0], SMALL_FIELD_SIZE, '<', data[0])
    last_point = format_data_point(data_format[-1], SMALL_FIELD_SIZE, '<', data[-1])
    for form, point in zip(data_format[1:-1], data[1:-1]):
        line += format_data_point(form, SMALL_FIELD_SIZE, '>', point)

    return line + last_point


def large_field_format_line(data_format, data, ident):
    data_format = copy.copy(data_format)
    data = copy.copy(data)

    line1 = format_data_point(data_format.pop(0), SMALL_FIELD_SIZE, '<', data.pop(0) + '*')
    for i in range(4):
        line1 += format_data_point(data_format.pop(0), LARGE_FIELD_SIZE, '^', data.pop(0))
    line1 += format_data_point(LITERAL, SMALL_FIELD_SIZE, '<', '*' + ident)

    line2 = format_data_point(LITERAL, SMALL_FIELD_SIZE, '<', '*' + ident)
    for i in range(4):
        line2 += format_data_point(data_format.pop(0), LARGE_FIELD_SIZE, '^', data.pop(0))
    line2 += format_data_point(data_format.pop(0), SMALL_FIELD_SIZE, '<', data.pop(0))

    return line1 + "\n" + line2


def _chunks(arr, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(arr), n):
        yield arr[i:i + n]


def dynamic_field_writer(command: str, fixed_data_type_array: [int], fixed_data_array: [],
                         dynamic_data_type: int, *args):
    lines = []
    form_list = list(_chunks(fixed_data_type_array + [dynamic_data_type for _ in range(len(args))], 8))
    data_list = list(_chunks(fixed_data_array + list(args), 8))
    size = len(form_list)
    if size == 1:
        empty_space = 8 - len(fixed_data_type_array) - len(args)
        form = [3] + form_list[0] + [0 for _ in range(empty_space)] + [0]  # COMMAND, ID, D1, D2, ... , ,
        data = [command] + data_list[0] + ['' for _ in range(empty_space)] + ['']
        lines.append(small_field_format_line(form, data))
    else:
        for i, zipped in enumerate(zip(form_list, data_list)):
            form = zipped[0]
            data = zipped[1]
            if i == 0:  # first line case
                p_form = [3] + form + [-1]
                p_data = [command] + data + ['']
                lines.append(small_field_format_line(p_form, p_data))
            elif i == size - 1:  # end line case
                empty_space = 8 - len(form)
                p_form = [-1] + form + [0 for _ in range(empty_space)] + [0]
                p_data = [''] + data + ['' for _ in range(empty_space)] + ['']
                lines.append(small_field_format_line(p_form, p_data))
            else:
                p_form = [-1] + form + [-1]
                p_data = [''] + data + ['']
                lines.append(small_field_format_line(p_form, p_data))
    return lines
