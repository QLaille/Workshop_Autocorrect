# Workshop Autocorrect
# Autocorrectors, what is this magic ?

## 1. Introduction

You don't know how these magical algorithms work, yet you use them everyday: with your phones, your softwares, for researches (the 'did you mean' of Google)...

First let’s consider what it does. It takes in a misspelled word — (for example ‘teh’ )  and returns the best guess at the correct spelling — (‘the’).

Such magic needs two components.

## 2. A "database"

To defines the words the algorithm must use, we need a reference that uses the most common words of the said language.
For this workshop, we will use [The Project Gutenberg EBook of The Adventures of Sherlock Holmes](https://norvig.com/big.txt).
By using this novel and parsing all the words, we can produce a word count, where 'the' is used 85039 times, 'it' 68904 times, 'a' 68598 times, etc.

## 3. List every possible errors

For this workshop, we can say that every error is one of the four following types. So if the user types ‘teh’ they could have meant to:

    add a letter: ‘teh’ -> ‘ateh, bteh, cteh, dteh,….,tehy, tehz’
    remove a letter: ‘teh’ -> ‘eh, te, th’
    substitute a letter: ‘teh’ -> ‘aeh, beh, ceh,…,tey, tez’
    switch two adjacent letters: ‘teh’ -> ‘hte, the’

> Notice that all those words only need to change 1 letter to become correct, we say that those words are words of error > > distance 1. A word of error distance 2 from ‘teh’ would be ‘too’ — ‘teh’ -> ‘toh’ -> ‘too’

## 4. Implement the algorithm

From now on, we have all required tools to build a spellchecker.
We just need to think of how it will work:

- Check if the word exists in our database
- If not, generate all possible words of error distance 1.
- Then, we pick the word from the list which is the most probable correct one, to stay simple the most common one in our database.

For instance, if the user input is 'thene', a possible correction of distance 1 is 'then', and 'the' of distance 2.
Even if 'the' is the most common word, it appears that the user probably wanted to type 'then'.

## 5. Let's code !

###### For this workshop, we write the autocorrect in python, but you can do it with whatever language you want. However, since we can interpret python, our reference for the 'database' will be loaded and parsed once, whereas with C or another language might need to open and parse it everytime we execute our program.

First of all, we import a library, for the use of regex (it helps you validating a password, a username, or finding a specific word in a string). The other library I import is because I'm lazy and I don't want to type the entire alphabet in a string.

> Our word of reference for this example will be 'corerct', which will be corrected to 'correct'.

#### A. The hard part

We start with the hardest part of the code: the generation of all possible words with a correction of distance 1.
We first get the alphabet in a string we will use.
```python
import string

def edits1(word):
	#We invoke the alphabet in a string
    alphabet    = string.ascii_lowercase
```

---

We want to split our word as pairs of characters to correct on every character to start editing it.
For example, with our word 'corerct', we will make the following list of tuple.
```
[
('', 'corerct'),
('c', 'orerct'),
('co', 'rerct')
...
('corerc', 't'),
('corerct', '')
]
```

> The first and last tuple of the list are important: what if we can correct the word by adding a character at the beginning > or the end of the word ?

*With an index going from the beginning to the end of the word, generate a tuple with what's on the left and what's on the right of this index.*

```python
  splits = []
  for i in range(len(word) +1):
    list.append( (word[:i], word[i:]) )
```

---

We now generate the list of all words with a letter removed.

*For all tuple of the list, remove a character from the right element.*

```python
deletes = []
for L, R in splits:
  if R:
    deletes.append( L + R[1:] )
```

---

We generate the list of all words with two letters swapped.

*For all tuple of the list, swap the first and the second character of the right part.*

```python
transposes = []
for L, R in splits:
  if len(R)>1:
    transposes.append( L + R[1] + R[0] + R[2:] )
```

---

We generate the list of all words with a letter replaced.

*For all tuple of the list, replace the first character of the right side with every letter of the alphabet*

```python
replaces = []
for L,R in splits:
  if R:
    for c in alphabet:
      replaces.append( L + c + R[1:] )
```
---

We finally generate the list of all words in which we inserted letters of the alphabet.

*For all tuple of the list, add every letter of the alphabet inbetween*

```python
inserts = []
for L,R in splits:
  for c in alphabet:
    inserts.append( L + c + R )
```

#### B. The easy part

Now we only need to implement functions to import our text of reference, to categorize every word by its probability to appear in the text and determine from our generated list of possible words which one the user might have wanted to use.

---

We import the Counter side of collections, a Counter is a container that keeps track of how many times equivalent values are added. We also import re for the use of regex (short for regular expression).

```python
import re
from collections import Counter
```

We define our reference file, and split it to get all words in a Counter called WORDS.

```python
REFERENCE_FILE = 'big.txt'

#Split a string by separators, such as spaces or carriage returns
def words(text):
  return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open(REFERENCE_FILE).read()))
```

We write a function which returns the probability of getting a word in WORDS,
this will be important in determining the most accurate word.
```python
def P(word):
    N = sum(WORDS.values())
    return WORDS[word] / N
```

We then write a function to get a list of words that appear in WORDS (and thus known from our spellchecker).

*For all word in words, add word to a list if it is in WORDS*
```python
def known(words):
    return set(w for w in words if w in WORDS)
```




We then write a function to generate all possible spelling corrections for a word in a set.

*Return the word if it is known, a list of all possible words from that word, else the word itself*
```python
def candidates(word):
    return (known([word]) or known(edits1(word)) or [word])
```

We finally want to write a function to pick the most accurate word based on its probability to appear in WORDS by using the function P.

*Return the best corrected word possible based on a word from the user*
```python
def correction(word):
    return max(candidates(word), key=P)
```

## 6. Now what ?

Now you can test it in your python interpreter !

`python -i myfile.py`

```
>>> correction('corerct')
'correct'
>>>
```

Congratulations, you've just made a spellchecker !

Okay, it is not perfect: If I run it with 400 words, at a speed of 35 words per second, it is accurate by almost 70%.

But as a proof of concept, it works just fine, but maybe you want to improve it :

- Implement a way of generating all words of error distance 2

- Find a better book or novel to have a more accurate usage of the english language, or maybe another language !

- Implement it with a compiled language: it will be much much faster

- Use the internet to sharpen your autocorrection !

You can find the entire code on [the repository of this workshop](https://github.com/QLaille/Workshop_Autocorrect)
