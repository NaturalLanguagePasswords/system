import re
import secrets

# Open the nlp dump
with open("nlp.sql") as f:
    data = f.readlines()
f.close()

# find the line that contains all the words
raw = ""
for line in data:
    if line.startswith("INSERT INTO `wordlist` VALUES "):
        raw = line.replace("INSERT INTO `wordlist` VALUES ", "")

# Compile words into adjectives and nouns
adjectives = []
nouns = []

# Seperate the blocks of words
raw_split = raw.split('),')

for word in raw_split:
    # find the adjectives and nouns
    word, adjective, noun, plural, nlp = re.findall(r"\w+", word)

    # if adjective, put it in the adjectives list
    if adjective == "1":
        adjectives.append(word)

    # if noun, put it in the nouns list
    if noun == "1":
        nouns.append(word)

# generate a bunch of random adjective-noun-adjective-noun combinations
for x in range(10):
    adj1 = secrets.choice(adjectives)
    nou1 = secrets.choice(nouns)
    adj2 = secrets.choice(adjectives)
    nou2 = secrets.choice(nouns)

    print(adj1, nou1, adj2, nou2)

# example output:
#    askew weed touchy creeks
#    spiffy admin urgent plans
#    festive skewers ripe lamb
#    safest wipe glum walmart
#    potent flattery snazzy loss
#    pleasant almanac nosy hood
#    lesser skiis grouped goblin
#    shaky lemurs trim looks
#    tough stardom wired soups
#    demur sear posh ritz
