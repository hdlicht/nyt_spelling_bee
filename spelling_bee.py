import numpy as np 
import string
import itertools
import re
import csv

alphabet = list(string.ascii_lowercase)

wordlist = open("usa.txt", "r") 
all_words = wordlist.read().split("\n")

def regex(set, middle, word):
    exp = "^[{s}]*{m}[{s}]*$".format(s=set, m=middle)
    return re.match(exp,word)

def playable(w):
    return len(w) > 3 and len(set(w)) < 8 and w.isalpha()

def pangram(w):
    return len(set(w)) == 7

game_words = list(filter(playable,all_words))
game_words = [(word, sorted(tuple(set(word))),(len(word) if len(word) > 4 else 1)+(len(set(word))==7)*7) for word in game_words]
pangrams = [(word,tuple(char_set)) for (word,char_set,score) in game_words if len(char_set)==7]
candidates = set([tuple(char_set) for (word,char_set)  in pangrams])
ct = len(candidates)
game_stats = []
for i,combo in enumerate(candidates):
    print("{i} of {count}".format(i=i+1, count=ct))
    combo = set(combo)    
    game_pangrams = [word for (word, char_set) in pangrams if set(char_set) == combo]
    for letter in combo:
        words = [(word, char_set, score) for (word, char_set, score) in game_words if set(char_set).issubset(combo) and letter in set(char_set)]
        points = np.array([score for (word, char_set, score) in words])
        game_stats.append(dict(set="".join(combo), middle=letter, pangrams = game_pangrams, word_count = len(words), total_points = np.sum(points)))

        


keys = game_stats[0].keys()
print(game_stats[:10])
with open('game_stats_usa.csv', 'w+', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(game_stats)