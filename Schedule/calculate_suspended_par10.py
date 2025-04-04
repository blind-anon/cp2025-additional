#!/usr/bin/env python3
from contextlib import ExitStack
from os.path import basename
from sys import argv, exit

result_mapping = {'unknown': 2, 'solved': 1, 'unsolvable': 0}
prefix_size = 4


def par10(filenames, limits, seed_lb, seed_ub, use_mean=True):
    use_total_limit = False

    if len(limits) == 1:
        use_total_limit = True
    elif len(filenames) != len(limits):
        raise Exception("Too many/few time limits provided for models.")

    header_row_not_skipped = True

    total_limit = sum(limits)

    wip_par10 = 0
    num_seeds = 0

    model_dict = dict()

    for i, file_name in enumerate(filenames):
        file_prefix = basename(file_name)[:prefix_size]
        if file_prefix not in model_dict:
            model_dict[file_prefix] = []
        model_dict[file_prefix].append(i)

    similar_models = dict()

    for _, ms in model_dict.items():
        for model in list(ms):
            similar_models[model] = list(ms)
            similar_models[model].remove(model)

    with ExitStack() as stack:
        files = [stack.enter_context(open(i, "r")) for i in filenames]

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

            if seeds[0] < seed_lb or seeds[0] > seed_ub:
                continue

            is_certain = False
            time_expended = 0

            for i in range(len(values)):
                time_taken = float(values[i][2])

                for other_model in similar_models[i]:
                    if other_model < i:
                        time_taken -= min(float(values[other_model][2]),
                                          limits[other_model])

                if not use_total_limit:
                    limit = limits[i]
                    if i == len(values) - 1:
                        limit += max(total_limit - time_expended, 0)
                    timed_out = float(time_taken) > limit
                    time_expended += min(time_taken, limit)
                else:
                    time_expended += time_taken
                    timed_out = time_expended > total_limit
                    if timed_out:
                        break

                certain = result_mapping[values[i][1]] < 2

                if not timed_out and certain:
                    is_certain = True
                    break

            if not is_certain:
                time_expended = 10 * sum(limits)

            wip_par10 += time_expended
            num_seeds += 1

    if use_mean:
        return wip_par10 / num_seeds
    else:
        return wip_par10


def usage():
    print(f"usage: {argv[0]} <filenames_string> <limit/s_string>"
          " <lowest_seed>")
    print("Where:")
    print(" - `filenames_string` is a css of filename paths in schedule order")
    print(" - `limit/s_string` is a css of timeout limits in schedule order"
          " or a single integer for total timeout for the entire schedule")


if __name__ == "__main__":
    if len(argv) < 4:
        usage()
        exit(1)

    highest_seed = 10000
    if len(argv) >= 5:
        highest_seed = int(argv[4])

    filenames_string = argv[1]
    limits_string = argv[2]
    lowest_seed = int(argv[3])

    filenames_inp = filenames_string.strip().split(",")
    limits_inp = [float(limit) for limit in
                  limits_string.strip().split(",")]

    print(f"{par10(filenames_inp, limits_inp, lowest_seed, highest_seed):.3f}")
