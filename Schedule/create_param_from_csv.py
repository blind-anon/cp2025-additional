#!/usr/bin/env python3
from contextlib import ExitStack
from sys import argv, exit
from os import listdir
from os.path import join, basename
from square_brakets_to_list import print_list_with_underscore_seperators

result_mapping = {'unknown': 2, 'solved': 1, 'unsolvable': 0}
prefix_size = 4


def create_param(dirname, param_name, seconds_multiplier=1,
                 time_limit=60 * 20):
    data_files = []
    file_extension = ".csv"
    variable_name = "data"

    for file in listdir(dirname):
        if file.endswith(file_extension):
            data_files.append(join(dirname, file))

    if len(data_files) == 0:
        raise Exception("No data files found")

    data_files.sort()

    model_dict = dict()
    next_model_key = 1
    model_ref_list = []

    for file_name in data_files:
        file_prefix = basename(file_name)[:prefix_size]
        if file_prefix not in model_dict:
            model_dict[file_prefix] = next_model_key
            next_model_key += 1
        model_ref_list.append(model_dict[file_prefix])

    print_list_with_underscore_seperators([basename(file_name) for file_name in data_files])

    header_row_not_skipped = True
    to_prepend = f"letting {variable_name} = [\n\t"

    with open(param_name, "w") as param_file:

        param_file.write(
            f"letting timeLimit be {time_limit * seconds_multiplier}\n")
        param_file.write(f"letting modelRef be {model_ref_list.__str__()}\n")

        with ExitStack() as stack:
            files = [stack.enter_context(open(i, "r")) for i in data_files]
            for rows in zip(*files):
                if header_row_not_skipped:
                    header_row_not_skipped = False
                    continue

                values = [row.strip().split(",") for row in rows]
                seeds = [int(row[0]) for row in values]

                while seeds.count(seeds[0]) != len(seeds):
                    max_seed = max(seeds)
                    for i in range(len(seeds)):
                        if seeds[i] == max_seed:
                            continue
                        next_row = next(files[i])
                        values[i] = next_row.strip().split(",")
                        seeds[i] = int(values[i][0])

                mapped = [
                    [
                        int(row[0]),
                        result_mapping[row[1]],
                        float(row[2]) * seconds_multiplier
                    ]
                    for row in values]

                param_file.write(f"{to_prepend}[")
                to_prepend = ",\n\t"

                inner_prepend = ""
                for row in mapped:
                    param_file.write(
                        f"{inner_prepend}[{row[1]},{int(round(row[2]))}]")
                    inner_prepend = ","

                param_file.write("]")

        param_file.write("]\n\n")


def usage():
    print(f"usage: {argv[0]} <data_dirname> <param_name>"
          "<?seconds_multiplier> <?time_limit_seconds>")


if __name__ == "__main__":
    if len(argv) < 3:
        usage()
        exit(1)
    elif len(argv) == 4:
        create_param(argv[1], argv[2], seconds_multiplier=int(argv[3]))
    elif len(argv) == 5:
        create_param(argv[1], argv[2], seconds_multiplier=int(argv[3]),
                     time_limit=int(argv[4]))
    else:
        create_param(argv[1], argv[2])
