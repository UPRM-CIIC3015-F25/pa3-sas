from Cards.Card import Card, Rank

# TODO (TASK 3): Implement a function that evaluates a player's poker hand.
#   Loop through all cards in the given 'hand' list and collect their ranks and suits.
#   Use a dictionary to count how many times each rank appears to detect pairs, three of a kind, or four of a kind.
#   Sort these counts from largest to smallest. Use another dictionary to count how many times each suit appears to check
#   for a flush (5 or more cards of the same suit). Remove duplicate ranks and sort them to detect a
#   straight (5 cards in a row). Remember that the Ace (rank 14) can also count as 1 when checking for a straight.
#   If both a straight and a flush occur in the same suit, return "Straight Flush". Otherwise, use the rank counts
#   and flags to determine if the hand is: "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind",
#   "Two Pair", "One Pair", or "High Card". Return a string with the correct hand type at the end.
def evaluate_hand(hand: list[Card]):
    def get_rank_value(card):
        r = card.rank
        return r.value if hasattr(r, "value") else r

    ranks = [get_rank_value(card) for card in hand]
    suits = [card.suit for card in hand]

    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1
    counts_sorted = sorted(rank_counts.values(), reverse=True)

    suit_counts = {}
    for s in suits:
        suit_counts[s] = suit_counts.get(s, 0) + 1
    is_flush = any(c >= 5 for c in suit_counts.values())

    def has_straight(rank_list):
        unique = sorted(set(rank_list))
        if len(unique) < 5:
            return False

        def check(seq):
            if len(seq) < 5:
                return False
            longest = 1
            current = 1
            for i in range(1, len(seq)):
                if seq[i] == seq[i - 1] + 1:
                    current += 1
                    if current >= 5:
                        return True
                elif seq[i] != seq[i - 1]:
                    current = 1
            return False

        if 14 in unique:
            low = [1 if r == 14 else r for r in unique]
            low = sorted(set(low))
            return check(unique) or check(low)
        else:
            return check(unique)

    is_straight = has_straight(ranks)

    is_straight_flush = False
    if is_flush:
        for suit, c in suit_counts.items():
            if c >= 5:
                suited_ranks = [get_rank_value(card) for card in hand if card.suit == suit]
                if has_straight(suited_ranks):
                    is_straight_flush = True
                    break

    if is_straight_flush:
        return "Straight Flush"
    if counts_sorted[0] == 4:
        return "Four of a Kind"
    if counts_sorted[0] == 3 and any(c >= 2 for c in counts_sorted[1:]):
        return "Full House"
    if is_flush:
        return "Flush"
    if is_straight:
        return "Straight"
    if counts_sorted[0] == 3:
        return "Three of a Kind"
    if counts_sorted[0] == 2 and counts_sorted[1] == 2:
        return "Two Pair"
    if counts_sorted[0] == 2:
        return "One Pair"
    return "High Card" # If none of the above, it's High Card
