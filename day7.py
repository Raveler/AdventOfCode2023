from collections import defaultdict
import re
from collections import Counter


card_values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
joker_card_values = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

char_to_strength = {}
joker_char_to_strength = {}
for i in range(len(card_values)):
    char_to_strength[card_values[i]] = i
    joker_char_to_strength[joker_card_values[i]] = i



def get_score(real_cards, cards):

    count_per_value = defaultdict(lambda: 0)
    for card in cards:
        count_per_value[card] += 1

    sets = defaultdict(lambda: 0)
    for card in count_per_value:
        sets[count_per_value[card]] += 1

    strength = 0
    if sets[2] == 1 and sets[3] == 0:
        strength = 1
    elif sets[2] == 2:
        strength = 2
    elif sets[3] == 1 and sets[2] == 0:
        strength = 3
    elif sets[2] == 1 and sets[3] == 1:
        strength = 4
    elif sets[4] == 1:
        strength = 5
    elif sets[5] == 1:
        strength = 6

    # differentiate between the different high cards
    for card in real_cards:
        strength = strength * 100 + card

    return strength


def replace_joker_and_get_score(real_cards, cards, idx):

    if idx >= len(cards):
        return [get_score(real_cards, cards)]

    # brute force - replace each joker by each other card in the set and calculate the original score
    if cards[idx] == 0:
        unique_cards = set(cards)
        all_scores = []

        # special case for only jokers
        if len(unique_cards) == 1:
            return [get_score(real_cards, cards)]

        for unique_card in unique_cards:
            if unique_card == 0:
                continue
            cards = list(cards)
            cards[idx] = unique_card
            all_scores.extend(replace_joker_and_get_score(real_cards, cards, idx+1))


        return all_scores

    else:
        return replace_joker_and_get_score(real_cards, cards, idx+1)

def get_joker_score(cards):

    all_scores = replace_joker_and_get_score(cards, cards, 0)
    print(cards)
    print(all_scores)
    return max(all_scores)


def puzzle1():
    f = open("input7-2.txt")
    lines = f.readlines()

    hands = []
    for line in lines:
        split = line.split(" ")
        print(split[0])

        cards = [char_to_strength[x] for x in split[0]]
        joker_cards = [joker_char_to_strength[x] for x in split[0]]
        hands.append({
            "cards": cards,
            "joker_cards": joker_cards,
            "bid": int(split[1]),
            "score": get_score(cards, cards),
            "joker_score": get_joker_score(joker_cards)
        })

    hands.sort(key=lambda x: x["score"])
    winnings = 0
    for i in range(len(hands)):
        rank = i+1
        winnings += rank * hands[i]["bid"]

    hands.sort(key=lambda x: x["joker_score"])
    joker_winnings = 0
    for i in range(len(hands)):
        rank = i + 1
        joker_winnings += rank * hands[i]["bid"]

    print("The winnings are " + str(winnings))
    print("The joker winnings are " + str(joker_winnings))



puzzle1()
