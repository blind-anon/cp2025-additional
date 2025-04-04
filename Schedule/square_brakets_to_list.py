#!/usr/bin/env python3
from sys import argv, exit


def usage():
    print(f"usage: {argv[0]} <filename>")


def square_brackets_to_list(filename):
    with open(filename, 'r') as file:
        for line in file:
            return line.strip().split("[")[1][:-1].split(", ")


def print_list_with_underscore_seperators(to_print):
    to_prepend = ""
    for e in to_print:
        if "_" in e:
            print(f"{to_prepend}{e.split('_')[0]}", end="")
        else:
            print(f"{to_prepend}{e}", end="")
        to_prepend = "_"


if __name__ == "__main__":
    if len(argv) < 2:
        usage()
        exit(1)
    else:
        print_list_with_underscore_seperators(square_brackets_to_list(argv[1]))
