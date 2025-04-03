from functools import cmp_to_key

from Card import (
    DUMMY_CARD,
    DUMMY_STAGE,
    N_CARDS_IN_SUIT,
    Card,
    _encoding_to_str,
    get_stage_comparator,
    rank_comparator,
)
from GameBoard import GameBoard

LETTING_PREFIX = "letting "
LETTING_SUFFIX_SOLUTION = " be "
LETTING_SUFFIX_PRARM = " = "
FOUNDATION_STAGE_STR = "foundation_stage"
FIRST_TABLEAU_STAGE_STR = "first_tableau_stage"
SECOND_TABLEAU_STAGE_STR = "second_tableau_stage"
FIRST_TABLEAU_PARENT_STR = "first_tableau_parent"
SECOND_TABLEAU_PARENT_STR = "second_tableau_parent"
STOCK_ORDER_STR = "stock_order"
KING_PILE_STR = "king_pile"
KING_PLAYED_SPACE_STAGE_STR = "king_played_space_stage"
TABLEAU_STR = "tableau"
STOCK_STR = "stock"


def parse_cards_from_file(filename: str):

    foundation_array = None
    first_tableau_array = None
    second_tableau_array = None
    first_tableau_parent_array = None
    second_tableau_parent_array = None
    king_pile_array = None
    king_played_space_stage_array = None
    stock_order_array = None

    with open(filename, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith(LETTING_PREFIX):
            line = line[len(LETTING_PREFIX) :]
            line = line.split(LETTING_SUFFIX_SOLUTION)
            variable = line[0]
            value = line[1].strip()
            if variable == FOUNDATION_STAGE_STR:
                foundation_array = map(int, value[1:-12].split(", "))
            elif variable == FIRST_TABLEAU_STAGE_STR:
                first_tableau_array = map(int, value[1:-12].split(", "))
            elif variable == SECOND_TABLEAU_STAGE_STR:
                second_tableau_array = map(int, value[1:-12].split(", "))
            elif variable == FIRST_TABLEAU_PARENT_STR:
                first_tableau_parent_array = map(int, value[1:-12].split(", "))
            elif variable == SECOND_TABLEAU_PARENT_STR:
                second_tableau_parent_array = map(int, value[1:-12].split(", "))
            elif variable == KING_PILE_STR:
                king_pile_array = list(map(int, value[1:-1].split(", ")))
            elif variable == KING_PLAYED_SPACE_STAGE_STR:
                king_played_space_stage_array = list(map(int, value[1:-1].split(", ")))
            elif variable == STOCK_ORDER_STR:
                stock_order_array = list(map(int, value[1:-1].split(", ")))

    if (
        foundation_array is None
        or first_tableau_array is None
        or second_tableau_array is None
        or first_tableau_parent_array is None
        or second_tableau_parent_array is None
        or king_pile_array is None
        or king_played_space_stage_array is None
        or stock_order_array is None
    ):
        raise ValueError("Not all values found in file")

    zipped_array = zip(
        foundation_array,
        first_tableau_array,
        second_tableau_array,
        first_tableau_parent_array,
        second_tableau_parent_array,
    )

    cards = []
    for encoding, (
        foundation,
        first_tableau,
        second_tableau,
        first_tableau_parent,
        second_tableau_parent,
    ) in enumerate(zipped_array):
        king_pile = None

        if encoding % N_CARDS_IN_SUIT == N_CARDS_IN_SUIT - 1:  # King
            first_tableau_parent = DUMMY_CARD
            second_tableau_parent = DUMMY_CARD
            king_pile = king_pile_array[encoding // N_CARDS_IN_SUIT]
            first_tableau = king_played_space_stage_array[encoding // N_CARDS_IN_SUIT]
            second_tableau = DUMMY_STAGE

        cards.append(
            Card(
                encoding,
                first_tableau,
                second_tableau,
                foundation,
                first_tableau_parent,
                second_tableau_parent,
                king_pile,
            )
        )

    return cards, stock_order_array


def parse_board_from_file(filename: str):

    tableau_str = None
    stock_array = None

    with open(filename, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith(LETTING_PREFIX):
            line = line[len(LETTING_PREFIX) :]
            line = line.split(LETTING_SUFFIX_PRARM)
            variable = line[0]
            value = None
            try:
                value = line[1].strip()[1:-1]
            except IndexError:
                pass

            if value is None:
                continue

            if variable == TABLEAU_STR:
                tableau_str = value[1:-1].split("], [")
            if variable == STOCK_STR:
                stock_array = list(map(int, value.split(", ")))

    if tableau_str is None or stock_array is None:
        raise ValueError("Tableau or stock not found in file")

    tableau_arr = []
    for pile in tableau_str:
        tableau_arr.append(list(map(int, pile.split(", "))))

    return tableau_arr, stock_array


def run(param_file, solution_file):
    tableau_int_arr, stock_int_array = parse_board_from_file(param_file)

    parsed_cards, stock_order_array = parse_cards_from_file(solution_file)

    zipped_stock_array = zip(stock_int_array, stock_order_array)

    stock_card_array = []

    for stock_card_int, stock_order in zipped_stock_array:
        dummy_card = Card(
            stock_card_int,
            DUMMY_STAGE,
            DUMMY_STAGE,
            DUMMY_STAGE,
            DUMMY_CARD,
            DUMMY_CARD,
        )
        for card in parsed_cards:
            if card == dummy_card:
                stock_card_array.append(card)
                card.stock_order = stock_order
                break

    tableau_card_array = []

    for tableau_pile in tableau_int_arr:
        tableau_pile_cards = []
        for tableau_card_int in tableau_pile:
            dummy_card = Card(
                tableau_card_int,
                DUMMY_STAGE,
                DUMMY_STAGE,
                DUMMY_STAGE,
                DUMMY_CARD,
                DUMMY_CARD,
            )
            for card in parsed_cards:
                if card == dummy_card:
                    tableau_pile_cards.append(card)
                    break
        tableau_card_array.append(tableau_pile_cards)

    board = GameBoard(tableau_card_array, stock_card_array)
    print(board)

    sorted_cards = parsed_cards.copy()

    stage_on = 0
    max_face_up_index = max(board.face_up_tableau_index)
    while stage_on < DUMMY_STAGE and max_face_up_index > -1:
        comparator = get_stage_comparator(stage_on)
        sorted_cards = sorted(sorted_cards, key=cmp_to_key(comparator))

        stage_on = sorted_cards[0].get_next_moved(stage_on)[0]
        print(f"\nStage: {stage_on}")

        cards_moved = []
        index_offset = 0
        while sorted_cards[index_offset].get_next_moved(stage_on)[0] == stage_on:
            cards_moved.append(sorted_cards[index_offset])
            index_offset += 1

        next_foundation_moves = []
        next_tableau_moves = []
        for card in cards_moved:
            next_parent, moved_to_foundation = card.get_next_parent(stage_on)
            if moved_to_foundation:
                next_foundation_moves.append(card)
            else:
                next_tableau_moves.append((card, next_parent))

        next_parents = set()
        for _, next_parent in next_tableau_moves:
            if next_parent != DUMMY_CARD:
                if next_parent in next_parents:
                    raise RuntimeError("Multiple cards moved to same tableau parent")
                next_parents.add(next_parent)

        next_foundation_moves = sorted(
            next_foundation_moves, key=cmp_to_key(board.board_comparator), reverse=True
        )

        next_tableau_moves = sorted(
            next_tableau_moves, key=cmp_to_key(move_to_rank_comparator), reverse=True
        )

        for card, parent in next_tableau_moves:
            try:
                success = board.move(card, parent)
            finally:
                if card.king_pile is None:
                    print(
                        f"Tableau move: {card.__repr__()}, moving to {_encoding_to_str(parent)}\n"
                    )
                else:
                    print(
                        f"Tableau move: {card.__repr__()}, moving to pile index {card.king_pile}\n"
                    )
            if not success:
                raise RuntimeError("Tableau move failed")

        for card in next_foundation_moves:
            success = board.move(card, None)
            print(f"Foundation move: {card.__repr__()}\n")
            if not success:
                raise RuntimeError("Foundation move failed")

        stage_on += 1
        print(board)
        max_face_up_index = max(board.face_up_tableau_index)

    print("Solved!")


def move_to_rank_comparator(one, two):
    return rank_comparator(one[0], two[0])


if __name__ == "__main__":

    from sys import argv

    if len(argv) != 3:
        raise ValueError("Usage: python parse_input.py <param_file> <solution_file>")

    run(argv[1], argv[2])
