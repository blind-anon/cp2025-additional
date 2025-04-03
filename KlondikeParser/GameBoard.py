from typing import List

from Card import DUMMY_CARD, DUMMY_KING_PILE, DUMMY_STAGE, N_CARDS_IN_SUIT, Card


class GameBoard:

    def __init__(self, tableau_array, stock_array):
        self.tableau_array: List[List[Card]] = tableau_array
        self.face_up_tableau_index = [len(pile) - 1 for pile in tableau_array]
        self.stock_array: List[Card] = stock_array

        self.foundation_array: List[List[Card]] = [[], [], [], []]

        self.stock_set = set(stock_array)
        self.tableau_set = set()
        self.stock_index_on = 2
        self.deal_n = 3

        for pile in tableau_array:
            self.tableau_set.update(pile)

    def __str__(self):
        return (
            f"Tableau: {self.tableau_array}\n"
            f"Face Up Tableau Index: {self.face_up_tableau_index}\n"
            f"Stock: {self.stock_array}\n"
            f"Stock Index On: {self.stock_index_on}\n"
            f"Foundation: {self.foundation_array}\n"
        )

    def move(self, card, parent_card):
        if not self.is_valid_move(card, parent_card):
            return False

        if parent_card is not None:  # tableau move
            return self.move_tableau(card, parent_card)
        else:  # foundation move
            return self.move_foundation(card)

    def move_foundation(self, card):
        if card in self.tableau_set:
            card_index = None
            card_pile = None
            card_pile_index = None

            for i, tableau_pile in enumerate(self.tableau_array):
                if card in tableau_pile:
                    card_index = tableau_pile.index(card)
                    card_pile = tableau_pile
                    card_pile_index = i
                    break

            if card_index is None or card_pile is None:
                raise RuntimeError("Card not found in tableau array")

            if card_index < self.face_up_tableau_index[card_pile_index]:
                raise RuntimeError("Card is not face up")

            if card_index != len(card_pile) - 1:
                raise RuntimeError("Card is not top of tableau pile")

            self.tableau_set.remove(card)
            self.foundation_array[card.suit].append(card)
            card_pile.pop()
            self.face_up_tableau_index[card_pile_index] = min(
                len(card_pile) - 1, self.face_up_tableau_index[card_pile_index]
            )
            return True

        if card in self.stock_set:
            card_index = self.stock_array.index(card)
            self.stock_index_on = card_index
            popped_card = self.stock_array.pop(card_index)
            self.foundation_array[popped_card.suit].append(popped_card)
            self.stock_index_on -= 1

            if self.stock_index_on < 0:
                self.stock_index_on = min(self.deal_n, len(self.stock_array)) - 1

            self.stock_set.remove(card)

            return True

    def move_tableau(self, card, parent_card):

        parent_pile = None

        if parent_card == DUMMY_CARD and card.king_pile is not None:  # king
            parent_pile = self.tableau_array[card.king_pile - 1]
            parent_pile_index = card.king_pile - 1
        else:
            dummy_parent_card = Card(
                parent_card,
                DUMMY_STAGE,
                DUMMY_STAGE,
                DUMMY_STAGE,
                DUMMY_CARD,
                DUMMY_CARD,
            )

            parent_pile_index = None
            for j, tableau_pile in enumerate(self.tableau_array):
                try:
                    if dummy_parent_card == tableau_pile[-1]:
                        parent_pile = tableau_pile
                        parent_pile_index = j
                        break
                except IndexError:
                    pass

        if parent_pile is None:
            raise RuntimeError("Parent card not found in tableau array")

        if card in self.tableau_set:

            card_index = None
            card_pile = None
            card_pile_index = None

            for i, tableau_pile in enumerate(self.tableau_array):
                if card in tableau_pile:
                    card_index = tableau_pile.index(card)
                    card_pile = tableau_pile
                    card_pile_index = i
                    break

            if card_pile_index == parent_pile_index:
                raise RuntimeError("A tableau card is moved to the same pile")

            if card_index is None or card_pile is None:
                raise RuntimeError("Card not found in tableau array")

            if card_index < self.face_up_tableau_index[card_pile_index]:
                raise RuntimeError("Card is not face up")

            temp_stack = []
            for i in range(len(card_pile) - card_index):
                temp_card = card_pile.pop()
                temp_stack.append(temp_card)
            while len(temp_stack) > 0:
                parent_pile.append(temp_stack.pop())

            self.face_up_tableau_index[card_pile_index] = min(
                len(card_pile) - 1, self.face_up_tableau_index[card_pile_index]
            )

            return True

        if card in self.stock_set:
            card_index = self.stock_array.index(card)
            self.stock_index_on = card_index
            popped_card = self.stock_array.pop(card_index)

            parent_pile.append(popped_card)
            self.stock_index_on -= 1

            if self.stock_index_on < 0:
                self.stock_index_on = min(self.deal_n, len(self.stock_array)) - 1

            self.tableau_set.add(card)
            self.stock_set.remove(card)

            return True

    def is_valid_move(self, card, parent_card):
        if parent_card is not None:
            return self.is_valid_tableau_move(card, parent_card)
        else:
            return self.is_valid_foundation_move(card)

    def is_valid_foundation_move(self, card):
        return self.is_valid_origin(card, True) and self.is_valid_foundation_destination

    def is_valid_foundation_destination(self, card):
        rank = card.rank
        suit = card.suit

        if len(self.foundation_array[suit]) == 0:
            return rank == 0

        return rank == self.foundation_array[suit][-1].rank + 1

    def is_valid_tableau_move(self, card, parent_card: int):
        return self.is_valid_origin(card) and self.is_valid_tableau_destination(
            card, parent_card
        )

    def is_valid_origin(self, card: Card, foundation_move: bool = False):
        if card in self.stock_set:
            return self.is_valid_stock_origin(card)

        if card in self.tableau_set:
            return self.is_valid_tableau_origin(card, foundation_move)

        return False

    def is_valid_tableau_origin(self, card: Card, foundation_move: bool = False):
        if card not in self.tableau_set:
            raise RuntimeError("Invalid tableau origin: Card not in tableau")

        for i, tableau_pile in enumerate(self.tableau_array):
            if card in tableau_pile:
                card_index = tableau_pile.index(card)

                if not foundation_move:
                    face_up = card_index >= self.face_up_tableau_index[i]
                    if not face_up:
                        raise RuntimeError(
                            "Invalid tableau origin: Card is not face up"
                        )
                    return face_up
                else:
                    card_top = card_index == len(tableau_pile) - 1
                    if not card_top:
                        raise RuntimeError("Card is not top of tableau pile")
                    return card_top

        raise RuntimeError("Invalid tableau origin: Card not found in tableau array")

    def is_valid_stock_origin(self, card: Card):

        if card not in self.stock_set:
            raise RuntimeError("Invalid stock origin: Card not in stock")

        future_stock_index = self.stock_index_on

        while future_stock_index < len(self.stock_array):
            try:
                if self.stock_array[future_stock_index] == card:
                    return True
            except IndexError:
                pass

            future_stock_index += self.deal_n

        try:
            if self.stock_array[-1] == card:
                return True
        except IndexError:
            pass

        future_stock_index = 2

        while future_stock_index < len(self.stock_array):
            try:
                if self.stock_array[future_stock_index] == card:
                    return True
            except IndexError:
                pass

            future_stock_index += self.deal_n

        raise RuntimeError("Invalid stock origin: Card not accessible in the stock")

    def is_valid_tableau_destination(self, card: Card, parent_card: int):
        if parent_card == DUMMY_CARD:
            if card.king_pile is not None:  # king

                if card.king_pile == DUMMY_KING_PILE:
                    return False

                return len(self.tableau_array[card.king_pile - 1]) == 0

            return False

        dummy_parent_card = Card(
            parent_card,
            DUMMY_STAGE,
            DUMMY_STAGE,
            DUMMY_STAGE,
            DUMMY_CARD,
            DUMMY_CARD,
        )

        if card.rank != dummy_parent_card.rank - 1:
            raise RuntimeError(
                "Invalid tableau destination: Card rank is not one less than parent card rank"
            )

        if card.suit % 2 == dummy_parent_card.suit % 2:
            raise RuntimeError(
                "Invalid tableau destination: Card and parent card have the same color"
            )

        if dummy_parent_card in self.stock_set:
            raise RuntimeError(
                "Invalid tableau destination: Parent card is in the stock"
            )

        if dummy_parent_card not in self.tableau_set:
            raise RuntimeError(
                "Invalid tableau destination: Parent card is not in the tableau"
            )

        parent_found = False
        for tableau_pile in self.tableau_array:
            try:
                if dummy_parent_card == tableau_pile[-1]:
                    parent_found = True
                    break
            except IndexError:
                pass

        if not parent_found:
            raise RuntimeError(
                "Invalid tableau destination: Parent card not found in tableau array"
            )

        return parent_found

    def board_comparator(self, card_one: Card, card_two: Card):

        card_one_in_tableau = card_one in self.tableau_set
        card_two_in_tableau = card_two in self.tableau_set

        if not card_one_in_tableau and not card_two_in_tableau:
            return card_one.stock_order - card_two.stock_order

        if card_one_in_tableau and card_two_in_tableau:
            card_one_pile_index = None
            card_two_pile_index = None

            for i, tableau_pile in enumerate(self.tableau_array):
                if card_one in tableau_pile:
                    card_one_pile_index = i
                if card_two in tableau_pile:
                    card_two_pile_index = i

            if card_one_pile_index == card_two_pile_index:
                return self.tableau_array[card_one_pile_index].index(
                    card_one
                ) - self.tableau_array[card_two_pile_index].index(card_two)

            return card_two.rank - card_one.rank

        if card_one.rank == card_two.rank:
            return -1 if card_one_in_tableau else 1

        return card_two.rank - card_one.rank
