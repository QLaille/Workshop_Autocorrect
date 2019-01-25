#regural expression library
import re

#used for the alphabet
import string

#A Counter is a container that keeps track of how many times equivalent values are added.
#It can be used to implement the same algorithms for which bag or multiset data structures are commonly used in other languages.
from collections import Counter

#Set up a list of words
def words(text): return re.findall(r'\w+', text.lower())

#Here, novel.txt is our file
REFERENCE_FILE = 'novel.txt'
WORDS = Counter(words(open(REFERENCE_FILE).read()))

# Probability of a word in WORDS
def Probability(word, N=sum(WORDS.values())):
    return WORDS[word] / N

#Get the most probable spelling correction for word from a set of all possible corrections
#A set is an unordered collection of items. Every element is unique (no duplicates) and must be immutable (which cannot be changed).
def correction(word):
    return max(candidates(word), key=Probability)

#Generate all possible spelling corrections for a word in a set.
def candidates(word):
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

# Get the subset of words that appear in the dictionary of WORDS in a set.
def known(words):
    return set(w for w in words if w in WORDS)

#Generate all possible outcomes that are one edit away from the word in a set.
def edits1(w):
	#We invoke the alphabet in a string
    letters    = string.ascii_lowercase

    split     = [(w[:i], w[i:])    for i in range(len(w) + 1)]			            #Make a list of tuple by spliting word at every index
	#For example, "oui" will make [('', 'oui'), ('o', 'ui'), ('ou', 'i'), ('oui', '')]
    delete    = [l + r[1:]               for l, r in split if r]                  #Removes a letter if there is at least one letter on the right side of the tuple
	# For example, ('', 'oui') will make 'ui', ('o', 'ui') 'oi' and ('ou','i') 'ou'.
    transpose = [l + r[1] + r[0] + r[2:] for l, r in split if len(r)>1]           #Swap two letters in the string
	#For example, ('', 'oui') will make 'uoi' and ('o','ui') 'oiu'.
    replace   = [l + c + r[1:]           for l, r in split if r for c in letters] #Replace a letter
	#For example, it will make a list of X + 'ui', 'o' + X + 'i' and 'ou' + X, where X can be any character of the alphabet.
    insert    = [l + c + r               for l, r in split for c in letters]      #Insert a letter
	#For example, it will make a list of X + 'oui', 'o' + X + 'ui', 'ou' + X + 'i' and 'oui' + X, where X can be any character of the alphabet.
    return set(delete + transpose + replace + insert)

#Generate all possible outcomes that are two edits away from the word in a set.
def edits2(word):
    return (edit2 for edit1 in edits1(word) for edit2 in edits1(edit1))