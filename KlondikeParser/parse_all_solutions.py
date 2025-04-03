from contextlib import redirect_stdout

from check_deal import run

DIRNAME = "noworryback_params_solutions"
PARSED_DIRNAME = "parsed_solutions"
PARSED_SOLUTION_FILENAME = "_parsed.txt"


def parse_all_solutions(seedfile):
    # Read the seed file
    with open(seedfile, "r") as seed_file:
        seed_lines = seed_file.readlines()

    # Parse the seed file
    for seed_line in seed_lines:
        seed = seed_line.strip()

        solution_file = f"{DIRNAME}/{seed}.solution"
        param_file = f"{DIRNAME}/{seed}.param"

        print(f"Parsing {seed}...")

        with open(
            f"{PARSED_DIRNAME}/{seed}{PARSED_SOLUTION_FILENAME}", "w"
        ) as parsed_file:
            with redirect_stdout(parsed_file):
                run(param_file, solution_file)


if __name__ == "__main__":
    from sys import argv

    if len(argv) != 2:
        raise ValueError("Usage: python parse_all_solutions.py <seed_file>")

    parse_all_solutions(argv[1])
