import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('/home/pawel/McGraw/v2/lib/spellcheck/big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    if len(word)>20:
        return word
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
    
def correct_text(text,ignore_digits=True):
    error = False
    mistakes = {}
    for word in text.split():
        word_correct = correct(word.lower()).upper()
        if word_correct != word and re.search("[0-9]",word) is None:
            mistakes[word] = word_correct
            error = True
        
    if error:
        text_words = []
        for word in text.split():
            text_words.append(mistakes.get(word,word))
        return " ".join(text_words)
    else:
        return text