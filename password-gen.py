import random
import json


def get_dice_num(dice):
    # Generate noun number
    dice_num = ''
    for x in range(dice):
        dice_num += str(random.randint(1, 6))
    return dice_num


def get_word(data, id):
    # Match dice number with word from the JSON list
    for i in data:
        if i['id'] == id:
            return i['word']


# Initialize 2 of each noun and adjectives
noun_1 = get_dice_num(5)
noun_2 = get_dice_num(5)
adj_1 = get_dice_num(4)
ajd_2 = get_dice_num(4)

# Open adjectives list
with open('./nlp-adjectives.json') as f1:
    adj_list = json.load(f1)
f1.close()

# Open noun list
with open('./nlp-nouns.json') as f2:
    noun_list = json.load(f2)
f2.close()

# Concatenate the words into a password
password = f"{get_word(adj_list, adj_1)} {get_word(noun_list, noun_1)} {get_word(adj_list, ajd_2)} {get_word(noun_list, noun_2)}"

# Print the password
print(password)
