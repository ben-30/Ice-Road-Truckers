import random

# globals

deck = []
num_cards = 52
possible_straights = [[1,2,3,4,5],[2,3,4,5,6],[3,4,5,6,7],[4,5,6,7,8],[5,6,7,8,9],[6,7,8,9,10],[7,8,9,10,11],[8,9,10,11,12],[9,10,11,12,13],[10,11,12,13,1]]
possible_royal_flushes = [[10,11,12,13,1],[23,24,25,26,14],[36,37,38,39,27],[49,50,51,52,40]]
eval_nums = {"straight":0, "flush":0, "full_house":0, 'four_of_a_kind':0, "straight_flush":0, "royal_flush":0, "five_of_a_kind":0}

# helper functions

def shuffle():
    global deck, num_cards
    deck.clear()
    num_cards = 52
    for card in range(num_cards):
        deck.append(card + 1)
        
def draw_card():
    global deck, num_cards
    if num_cards == 0:
        return("No More Cards!")
    index = random.randint(0, num_cards - 1)
    card = deck[index]
    del deck[index]
    num_cards -= 1
    return card
    
def get_value(card):
    if card % 13 == 0:
        return 13
    return card % 13
    
def get_suit(card):
    if card <= 13:
        return 'c'
    elif card <= 26:
        return 'd'
    elif card <= 39:
        return 'h'
    elif card <= 52:
        return 's'
        
def get_card(card):
    value = get_value(card)
    if value == 11:
        value = 'J'
    elif value == 12:
        value = 'Q'
    elif value == 13:
        value = 'K'
    elif value == 1:
        value = 'A'
    else:
        value = str(value)
        
    return str(value + get_suit(card))
    
def print_cards(cards, preface = ""):
    if preface != "":
        print(preface)
    cards.sort()
    print(cards)
    actual_cards = []
    for actual_card in cards:
        actual_cards.append(get_card(actual_card))
    print(actual_cards)
    
# hand evaluation

def is_straight(cards, wildcards = 0):
    if len(cards) + wildcards < 5:
        return False
    cards.sort()
    values = []
    for card in cards:
        values.append(get_value(card))
    values = list(set(values))
    
    for straight in possible_straights:
        count = 0
        for num in straight:
            if num in values:
                count += 1
        if count >= 5 - wildcards:
            return True
    return False
    
def is_royal_flush(cards, wildcards = 0):
    cards.sort()
    for royal_flush in possible_royal_flushes:
        count = 0
        for num in royal_flush:
            if num in cards:
                count += 1
        if count >= 5 - wildcards:
            eval_nums["royal_flush"] += 1
    
def is_flush(cards, wildcards = 0):
    cards.sort()
    suits = {}
    for card in cards:
        suit = get_suit(card)
        if suit in suits:
            suits[suit] += 1
        else:
            suits[suit] = 1
    for value in suits.values():
        if value >= 5 - wildcards:
            return True
    return False
    
def is_straight_flush(cards, wildcards = 0):
    cards.sort()
    clubs = []
    diamonds = []
    hearts = []
    spades = []
    
    for card in cards:
        if get_suit(card) == 'c':
            clubs.append(card)
        elif get_suit(card) == 'd':
            diamonds.append(card)
        elif get_suit(card) == 'h':
            hearts.append(card)
        elif get_suit(card) == 's':
            spades.append(card)
    
    if is_straight(clubs, wildcards) or is_straight(diamonds, wildcards) or is_straight(hearts, wildcards) or is_straight(spades, wildcards):
        return True
    return False
    
def same_cards(cards, wildcards = 0):
    values = {}
    five_of_a_kind = False
    four_of_a_kind = False
    three_of_a_kind = False
    pair = False
    
    for card in cards:
        value = get_value(card)
        if value in values:
            values[value] += 1
        else:
            values[value] = 1
    for value in values.values():
        if value >= 5 - wildcards:
            five_of_a_kind = True
        if value >= 4 - wildcards:
            four_of_a_kind = True
        if wildcards == 1:
            if value >= 3:
                three_of_a_kind = True
                pair = True
            elif value == 2:
                if three_of_a_kind == False:
                    three_of_a_kind = True
                else:
                    pair = True
        elif wildcards == 2:
            if value >= 2:
                    three_of_a_kind = True
                    pair = True
        else:
            three_of_a_kind = True
            pair = True
            
    if five_of_a_kind:
        eval_nums["five_of_a_kind"] += 1
    if four_of_a_kind:
        eval_nums["four_of_a_kind"] += 1
    if three_of_a_kind and pair:
        eval_nums["full_house"] += 1
    
def evaluate(board, hand):
    min_value = 15
    wildcards = 0
    eval_cards = []
    
    for card in board:
        value = get_value(card)
        if value != 1:
            if value < min_value:
                min_value = value
    for card in board + hand:
        value = get_value(card)
        if value == min_value:
            wildcards += 1
        else:
            eval_cards.append(card)
    
    if (is_straight(eval_cards, wildcards)):
        eval_nums["straight"] += 1
    if (is_flush(eval_cards, wildcards)):
        eval_nums["flush"] += 1
    if (is_straight_flush(eval_cards, wildcards)):
        eval_nums["straight_flush"] += 1
    if (is_royal_flush(eval_cards, wildcards)):
        eval_nums["royal_flush"] += 1
    same_cards(eval_cards, wildcards)
    
# simulation

for i in range(1000000):
    shuffle()
    board = []
    hand = []
    for _ in range(5): board.append(draw_card())
    for _ in range(2): hand.append(draw_card())
    evaluate(board, hand)
    
print(eval_nums)