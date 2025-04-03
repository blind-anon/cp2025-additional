DUMMY_STAGE = 80
DUMMY_CARD = 52
DUMMY_KING_PILE = 0
N_CARDS_IN_SUIT = 13
N_SUITS = 4

RANK_MAP = {
    0: "A",
    1: "2",
    2: "3",
    3: "4",
    4: "5",
    5: "6",
    6: "7",
    7: "8",
    8: "9",
    9: "10",
    10: "J",
    11: "Q",
    12: "K",
}

SUIT_MAP = {
    0: "♠",
    1: "♥",
    2: "♣",
    3: "♦",
}


class Card:

    def __init__(
        self,
        encoding,
        first_tableau_stage,
        second_tableau_stage,
        foundation_stage,
        first_tableau_parent,
        second_tableau_parent,
        king_pile=None,
    ):

        self.encoding = encoding
        self.first_tableau_stage = first_tableau_stage
        self.second_tableau_stage = second_tableau_stage
        self.foundation_stage = foundation_stage
        self.first_tableau_parent = first_tableau_parent
        self.second_tableau_parent = second_tableau_parent
        self.king_pile = king_pile
        self.stock_order = None

        self.suit = encoding // N_CARDS_IN_SUIT
        self.rank = encoding % N_CARDS_IN_SUIT

        moved_stages = []
        stage_second_moved = None
        stage_third_moved = None

        if self.rank != N_CARDS_IN_SUIT - 1:  # Not a king
            if first_tableau_parent == DUMMY_CARD:
                self.first_tableau_parent = DUMMY_STAGE
                self.second_tableau_parent = DUMMY_STAGE
            elif second_tableau_parent == DUMMY_CARD:
                self.second_tableau_parent = DUMMY_STAGE

        if foundation_stage == first_tableau_stage:
            first_tableau_stage = DUMMY_STAGE
            self.first_tableau_stage = DUMMY_STAGE
            self.first_tableau_parent = DUMMY_CARD
            second_tableau_stage = DUMMY_STAGE
            self.second_tableau_stage = DUMMY_STAGE
            self.second_tableau_parent = DUMMY_CARD

        if foundation_stage == second_tableau_stage:
            second_tableau_stage = DUMMY_STAGE
            self.second_tableau_stage = DUMMY_STAGE
            self.second_tableau_parent = DUMMY_CARD

        if first_tableau_stage != DUMMY_STAGE:
            stage_first_moved = first_tableau_stage
            moved_stages.append(first_tableau_stage)
            if second_tableau_stage != DUMMY_STAGE:
                stage_second_moved = second_tableau_stage
                stage_third_moved = foundation_stage
                moved_stages.append(second_tableau_stage)
                moved_stages.append(foundation_stage)
                foundation_moved = 3
            else:
                stage_second_moved = foundation_stage
                moved_stages.append(foundation_stage)
                foundation_moved = 2
        else:
            stage_first_moved = foundation_stage
            moved_stages.append(foundation_stage)
            foundation_moved = 1

        self.stage_first_moved = stage_first_moved
        self.stage_second_moved = stage_second_moved
        self.stage_third_moved = stage_third_moved
        self.moved_stages = moved_stages
        self.foundation_moved = foundation_moved

    def __eq__(self, other):
        return self.encoding == other.encoding

    def __hash__(self):
        return hash(self.encoding)

    def __str__(self):

        first_tableau_parent = (
            None
            if self.rank == N_CARDS_IN_SUIT - 1
            or self.first_tableau_parent == DUMMY_CARD
            else self.first_tableau_parent
        )
        second_tableau_parent = (
            None
            if self.rank == N_CARDS_IN_SUIT - 1
            or self.second_tableau_parent == DUMMY_CARD
            else self.second_tableau_parent
        )

        repr = (
            f"{_encoding_to_str(self.encoding)}: "
            f"Stages moved: {self.moved_stages}, "
            f"Foundation moved: {self.foundation_moved}"
        )

        if first_tableau_parent is not None:
            repr += f", First tableau parent: {_encoding_to_str(first_tableau_parent)}"

        if second_tableau_parent is not None:
            repr += (
                f", Second tableau parent: {_encoding_to_str(second_tableau_parent)}"
            )

        return repr

    def __repr__(self):
        return _encoding_to_str(self.encoding)

    def get_next_moved(self, stage):
        """
        Get the next stage the card moved to after the given stage
        :param stage: The stage after which to find the next moved stage
        :return: The next moved stage and whether the card was moved to the foundation
        """
        moves = self.moved_stages.copy()
        move = 1
        while len(moves) > 0 and stage > moves[0]:
            moves.pop(0)
            move += 1

        if len(moves) == 0:
            return DUMMY_STAGE, False
        return moves[0], move == self.foundation_moved

    def get_next_parent(self, stage):
        """
        Get the next parent the card moved to after the given stage
        :param stage: The stage after which to find the next parent
        :return: The next parent stage
        """
        stage_moved, foundation_move = self.get_next_moved(stage)

        if stage_moved == DUMMY_STAGE:
            return DUMMY_CARD, False

        if stage_moved == self.first_tableau_stage:
            return self.first_tableau_parent, False
        if stage_moved == self.second_tableau_stage:
            return self.second_tableau_parent, False
        if stage_moved == self.foundation_stage:
            return DUMMY_CARD, True


def get_stage_comparator(stage):
    return lambda one, two: one.get_next_moved(stage)[0] - two.get_next_moved(stage)[0]


def rank_comparator(one, two):
    return one.rank - two.rank


def _encoding_to_str(encoding):
    suit = encoding // N_CARDS_IN_SUIT
    rank = encoding % N_CARDS_IN_SUIT
    return f"{RANK_MAP[rank]}{SUIT_MAP[suit]}"
