#!/usr/bin/env python3
from sys import argv, exit
from os import listdir
from os.path import join
from square_brakets_to_list import square_brackets_to_list
from calculate_suspended_fraction_certain import fraction_certain

result_mapping = {'unknown': 2, 'solved': 1, 'unsolvable': 0}


def parse_to_fraction_certain(data_dir, order_file, timeout_file, seed_lb, seed_ub,
                              seconds_multiplier):
    data_files = []
    file_extension = ".csv"

    for file in listdir(data_dir):
        if file.endswith(file_extension):
            data_files.append(join(data_dir, file))

    if len(data_files) == 0:
        raise Exception("No data files found")

    data_files.sort()

    order = [int(i) for i in square_brackets_to_list(order_file)]
    timeouts = [float(i) / seconds_multiplier for i in
                square_brackets_to_list(timeout_file)]

    schedule_size = len(order)

    schedule_filenames = [""] * schedule_size
    schedule_timeouts = [0] * schedule_size

    for i in range(len(order)):
        schedule_filenames[order[i] - 1] = data_files[i]
        schedule_timeouts[order[i] - 1] = timeouts[i]

    for i in range(len(order) - 1, -1, -1):
        if schedule_timeouts[i] == 0:
            del schedule_timeouts[i]
            del schedule_filenames[i]

    fraction = fraction_certain(schedule_filenames, schedule_timeouts, seed_lb,
                                seed_ub)

    return fraction


def usage():
    print(f"usage: {argv[0]} <data_dirname> <order_filename> "
          "<timeout_filename> <seed_lower_bound> <seed_upper_bound> "
          "<seconds_multiplier>")


if __name__ == "__main__":
    if len(argv) < 7:
        usage()
        exit(1)
    else:
        score = parse_to_fraction_certain(argv[1], argv[2], argv[3], int(argv[4]),
                                          int(argv[5]), int(argv[6]))
        print(f"{score * 100:.3f}%")
