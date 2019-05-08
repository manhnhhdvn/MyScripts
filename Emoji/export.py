# -*- coding: utf-8 -*-

import json
import re
import xlwt
import sys
from prettytable import PrettyTable

def is_regional_indicator_symbol(hex_str):
    hex_int = int(hex_str, 16)
    regional_indicator_symbol_a_hex_int = int("0x1F1E6", 16)
    regional_indicator_symbol_z_hex_int = int("0x1F1FF", 16)
    return (regional_indicator_symbol_a_hex_int <= hex_int and hex_int <= regional_indicator_symbol_z_hex_int)

def is_number_of_other(hex_str):
    hex_int = int(hex_str, 16)
    return hex_int == 35 or hex_int == 42 or (48 <= hex_int and hex_int <= 57)

def load_file_data(src_file):
    read_file_pointer = open(src_file, "r")
    base_emoji_list = []
    for line in read_file_pointer:
        if line.startswith("#") or line == "\n":
            continue
        line_value = line.split(";")[0].strip()
        base_emoji = line_value.split(" ")[0].strip()
        base_emoji_list.append(str(base_emoji))
    result = sorted(list(dict.fromkeys(base_emoji_list)))
    print(result)
    print(len(result))
    return result

def export_to_file(data_to_export):
    count = 0
    write_file_pointer= open("result.txt","w+")
    write_file_pointer.write("[")
    for value in data_to_export:
        count += 1
        if is_regional_indicator_symbol(value) or is_number_of_other(value):
            continue
        write_file_pointer.write("0x{}".format(value))
        if count != len(data_to_export):
            write_file_pointer.write(", ")
    write_file_pointer.write("]")
    print(count)
    write_file_pointer.close()

if __name__ == "__main__":
    data = load_file_data("all_emoji.txt")
    export_to_file(data)
    