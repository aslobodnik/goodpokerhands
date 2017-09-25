from itertools import  permutations,combinations,combinations_with_replacement
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    all_hands = generate_possible_hands() 
    return render_template('home_page.html',all_hands=all_hands)
    

@app.route('/texas-holdem/<hand>')
def render_hand_statistics(hand):
    """Creates a page for every starting hand in texas holdem 
    generalized hands such as:
    67s --> six-seven suited
    67o --> six-seven offsuite
    67  --> six-seven both suited & offsuit
    AA  --> aces"""
    
    all_hands = generate_possible_hands() 
    
    return render_template('preflop_hand_profile.html',hand=hand.split('-')[0],all_hands=all_hands)

#def generate_hand_links():
    


@app.route("/hand_compare/<hand_1>_vs_<hand_2>")
def hand_generator(hand_1,hand_2):
    probability_hand_1 = probability_of_hand(hand_1)
    probability_hand_2 = probability_of_hand(hand_2)
    
    hands_1 = generate_hand_comparision()
    hands_2 = generate_hand_comparision()
    
    return render_template('basic.html',hand_1=hand_1,hand_2=hand_2
            ,probability_hand_2=probability_hand_2
            ,probability_hand_1=probability_hand_1
            ,hands_1=hands_1,hands_2=hands_2)

@app.context_processor
def utility_processor():
    def format_percent(float_decimal):
        return u'{0:.2f}%'.format(float_decimal*100)
    def format_percent1(float_decimal):
        return u'{0:.1f}%'.format(float_decimal*100)
    def long_name(hand):
        names = {'a':'Ace','k':'King','q':'Queen','j':'Jack','t':'Ten','9':'Nine'
                ,'8':'Eight','7':'Seven','6':'Six','5':'Five','4':'Four'
                ,'3':'Three','2':'Two'}
        if hand[0] == hand[1]:
            if names[hand[0]] == 'six':
                return 'sixes'
            else:
                return names[hand[0]] + 's'
        else:
            if hand[-1] == 'o':
                return names[hand[0]] + '-' + names[hand[1]] + ' offsuit'
            elif hand[-1] == 's':
                return names[hand[0]] + '-' + names[hand[1]] + ' suited'
            else:
                return names[hand[0]] + '-' + names[hand[1]]
            
    def long_name_1(hand):
        names = {'a':'ace','k':'king','q':'queen','j':'jack','t':'ten','9':'nine'
                ,'8':'eight','7':'seven','6':'six','5':'five','4':'four'
                ,'3':'three','2':'two'}
        if hand[0] == hand[1]:
            if names[hand[0]] == 'six':
                return 'Sixes'
            else:
                return names[hand[0]] + 's'
        else:
            if hand[-1] == 'o':
                return names[hand[0]] + '-' + names[hand[1]] + '-offsuit'
            elif hand[-1] == 's':
                return names[hand[0]] + '-' + names[hand[1]] + '-suited'
            else:
                return names[hand[0]] + '-' + names[hand[1]]
    
    def capitalize_hand(hand):
        """Changes aks --> AKs"""
        if len(hand) == 2:
            return hand.upper()
        elif len(hand) == 3:
            return hand[:2].upper() + hand[2]
    
    def display_probility_of_hand_being_dealt(hand):
        return probability_of_hand(hand)
    
    def win_percent(hand):
        return WIN_VS_RANDOM[hand]
                                
    return dict(format_percent=format_percent,long_name=long_name,long_name_1=long_name_1
                ,capitalize_hand=capitalize_hand
                ,display_probility_of_hand_being_dealt=display_probility_of_hand_being_dealt
                ,format_percent1=format_percent1
                ,win_percent=win_percent)


def probability_of_hand(hand):

    suited = hand[-1] == 's'
    off_suit = hand[-1] == 'o'
    pocket_pair = hand[0] == hand[1]
    probability = 0.0

    if suited:
        probability = (8/52)*(1/51)
    elif off_suit:
        probability = (8/52)*(3/51)
    elif pocket_pair:
        probability = (4/52)*(3/51)
    else:
        probability = (8/52)*(4/51)
    return probability

def get_stats(hand):
    """Returns statistics about a hand"""
    return HAND_LOOKUP[hand]

def generate_possible_hands():
    """Creates a list of all possible starting hands in holdem, ignoring suit.
    Differintiates between suited, offsuit, and unspecified
    AK, AKo, and AKs"""
    
    values = 'akqjt98765432'
    types = ['','s','o']
    
    final_hands = []
    
    hands = combinations(values,2)
    hands = [''.join(hand) for hand in hands]
    for hand in hands:
        for t in types:
            final_hands.append(hand+t)
    pockets = [a*2 for a in values]
    final_hands = pockets + final_hands
    return final_hands

def generate_hand_comparision():
    hands = generate_possible_hands()
    hand_comparision = combinations_with_replacement(hands,2)
    return hand_comparision



WIN_VS_RANDOM = {'aa':'85.3%',
'aks':'67.0%',
'ako':'65.4%',
'aqs':'66.1%',
'aqo':'64.5%',
'ajs':'65.4%',
'ajo':'63.6%',
'ats':'64.7%',
'ato':'62.9%',
'a9s':'63.0%',
'a9o':'60.9%',
'a8s':'62.1%',
'a8o':'60.1%',
'a7s':'61.1%',
'a7o':'59.1%',
'a6s':'60.0%',
'a6o':'57.8%',
'a5s':'59.9%',
'a5o':'57.7%',
'a4s':'58.9%',
'a4o':'56.4%',
'a3s':'58.0%',
'a3o':'55.6%',
'a2s':'57.0%',
'a2o':'54.6%',
'kk':'82.4%',
'kqs':'63.4%',
'kqo':'61.4%',
'kjs':'62.6%',
'kjo':'60.6%',
'kts':'61.9%',
'kto':'59.9%',
'k9s':'60.0%',
'k9o':'58.0%',
'k8s':'58.5%',
'k8o':'56.3%',
'k7s':'57.8%',
'k7o':'55.4%',
'k6s':'56.8%',
'k6o':'54.3%',
'k5s':'55.8%',
'k5o':'53.3%',
'k4s':'54.7%',
'k4o':'52.1%',
'k3s':'53.8%',
'k3o':'51.2%',
'k2s':'52.9%',
'k2o':'50.2%',
'qq':'79.9%',
'qjs':'60.3%',
'qjo':'58.2%',
'qts':'59.5%',
'qto':'57.4%',
'q9s':'57.9%',
'q9o':'55.5%',
'q8s':'56.2%',
'q8o':'53.8%',
'q7s':'54.5%',
'q7o':'51.9%',
'q6s':'53.8%',
'q6o':'51.1%',
'q5s':'52.9%',
'q5o':'50.2%',
'q4s':'51.7%',
'q4o':'49.0%',
'q3s':'50.7%',
'q3o':'47.9%',
'q2s':'49.9%',
'q2o':'47.0%',
'jj':'77.5%',
'jts':'57.5%',
'jto':'55.4%',
'j9s':'55.8%',
'j9o':'53.4%',
'j8s':'54.2%',
'j8o':'51.7%',
'j7s':'52.4%',
'j7o':'49.9%',
'j6s':'50.8%',
'j6o':'47.9%',
'j5s':'50.0%',
'j5o':'47.1%',
'j4s':'49.0%',
'j4o':'46.1%',
'j3s':'47.9%',
'j3o':'45.0%',
'j2s':'47.1%',
'j2o':'44.0%',
'tt':'75.1%',
't9s':'54.3%',
't9o':'51.7%',
't8s':'52.6%',
't8o':'50.0%',
't7s':'51.0%',
't7o':'48.2%',
't6s':'49.2%',
't6o':'46.3%',
't5s':'47.2%',
't5o':'44.2%',
't4s':'46.4%',
't4o':'43.4%',
't3s':'45.5%',
't3o':'42.4%',
't2s':'44.7%',
't2o':'41.5%',
'99':'72.1%',
'98s':'51.1%',
'98o':'48.4%',
'97s':'49.5%',
'97o':'46.7%',
'96s':'47.7%',
'96o':'44.9%',
'95s':'45.9%',
'95o':'42.9%',
'94s':'43.8%',
'94o':'40.7%',
'93s':'43.2%',
'93o':'39.9%',
'92s':'42.3%',
'92o':'38.9%',
'88':'69.1%',
'87s':'48.2%',
'87o':'45.5%',
'86s':'46.5%',
'86o':'43.6%',
'85s':'44.8%',
'85o':'41.7%',
'84s':'42.7%',
'84o':'39.6%',
'83s':'40.8%',
'83o':'37.5%',
'82s':'40.3%',
'82o':'36.8%',
'77':'66.2%',
'76s':'45.7%',
'76o':'42.7%',
'75s':'43.8%',
'75o':'40.8%',
'74s':'41.8%',
'74o':'38.6%',
'73s':'40.0%',
'73o':'36.6%',
'72s':'38.1%',
'72o':'34.6%',
'66':'63.3%',
'65s':'43.2%',
'65o':'40.1%',
'64s':'41.4%',
'64o':'38.0%',
'63s':'39.4%',
'63o':'35.9%',
'62s':'37.5%',
'62o':'34.0%',
'55':'60.3%',
'54s':'41.1%',
'54o':'37.9%',
'53s':'39.3%',
'53o':'35.8%',
'52s':'37.5%',
'52o':'33.9%',
'44':'57.0%',
'43s':'38.0%',
'43o':'34.4%',
'42s':'36.3%',
'42o':'32.5%',
'33':'53.7%',
'32s':'35.1%',
'32o':'31.2%',
'22':'50.3%'}