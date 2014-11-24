import re
import string

# replaces text numbers with numbers

SMALL_NUMBERS = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,

    'thir-teen': 13,
    'four-teen': 14,
    'fif-teen': 15,
    'six-teen': 16,
    'seven-teen': 17,
    'eigh-teen': 18,
    'nineteen': 19,


    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90
}

FRACTIONS = {
     'thirds': 3
    ,'thirdths': 3 # spelling
    ,'fourths': 4
    ,'fifths': 5
    ,'sixths': 6
    ,'sevenths': 7
    ,'eighths': 8
    ,'ninths': 9
    ,'tenths': 10
    ,'elevenths': 11
    ,'twelfths': 12
}

def text2num(t):
    return " ".join([str(SMALL_NUMBERS.get(w.lower(),w)) for w in t.split()])
        
def text2num_test():
    for k,v in SMALL_NUMBERS.items():
        assert text2num(k)==str(v)
    assert text2num("it is correct because it is one hire")=="it is correct because it is 1 hire"
    assert text2num("YES I DID IT ON MY PICE OF PAPER AND TWO FOURTHS IS GREATERTHAN TWO THIRDS")=="YES I DID IT ON MY PICE OF PAPER AND 2 FOURTHS IS GREATERTHAN 2 THIRDS"    
    
def replace_whole_words(t,findrepl):
    for find, repl in findrepl:
        t = " ".join([repl if k == find else k for k in t.split()])

    return t
    
def replace_whole_words_test():
    test_cases = [
         ("THIS IS A TEXT TO REPLACE",[],"THIS IS A TEXT TO REPLACE")
        ,("THIS IS A TEXT TO REPLACE",[["TEXT","WORD"],],"THIS IS A WORD TO REPLACE")
        ,("THIS IS A TEXT2 TO REPLACE",[["TEXT","WORD"],],"THIS IS A TEXT2 TO REPLACE")
    ]    

    for t1,findrepl,t2 in test_cases:
        assert replace_whole_words(t1,findrepl)==t2
    
def convert_word_fractions(t):
    t = text2num(t)
    fractions_denominators = map(string.upper,FRACTIONS.keys())
    
    # replaces "3rds -> THIRDS", "4ths -> FOURTHS" etc
    t = replace_whole_words(t,[("3RDS","THIRDS")
                              ,("4THS","FOURTHS")
                              ,("5THS","FIFTHS")    
                              ,("6THS","SIXTHS")
                              ,("7THS","SEVENTHS")
                              ,("8THS","EIGHTHS")
                              ,("9THS","NINTHS")
                              ,("10THS","TENTHS")
                              ,("HALF","1/2")])
    
    # replaces "2 fourths" -> "2/4"
    matches = re.findall("([0-9]+) ([a-zA-Z]+)",t,re.DOTALL | re.IGNORECASE)
    for nom,denom in matches:
        if denom in fractions_denominators:
            t = t.replace("%s %s" % (nom,denom), "%s/%s" % (nom,str(FRACTIONS[denom.lower()])))

    # replaces "2 out of 4" -> "2/4"
    matches = re.findall("([0-9]+) OUT OF ([0-9]+)",t,re.DOTALL | re.IGNORECASE)
    for nom,denom in matches:
        t = t.replace("%s OUT OF %s" % (nom,denom), "%s/%s" % (nom,denom))
    
    # replaces alone "thirds -> 1/3", "fourths -> 1/4"
    for k,v in FRACTIONS.items():
        t = t.replace(k.upper(),"1/%s" % (str(v)))
        
    # replacements whole words
    

    return t
    
def convert_word_fractions_test():
    
    test_cases = [
        "HE IS NOT CORRECT TWO THIRDS HAVE BIGGER PIECES"
       ,"NO BECAUSE 2 OUT OF FOUR IS GREATER THAN 2 OUT OF 3"
       ,"NO BECAUSE 2 3RDS IS BIGGER THAN 2 4THS"
       ,"NO 3RDS IS BIGGER THAN 4THS JUST BECAUSE THEY ARE BOTH 2 YOU ALSO HAVE TO LOOK AT THE DENOMINATER"
       ,'YES STANLEY IS RIGHT BECAUSE TWO THIRDTHS IS ONE OFF OF TWO FOURTHS'
    ]    

    for t in test_cases:
        print t
        print convert_word_fractions(t)
        print
    
    #assert convert_word_fractions("HE IS NOT CORRECT TWO THIRDS HAVE BIGGER PIECES") == "HE IS NOT CORRECT 2/3 HAVE BIGGER PIECES"
    
def text_to_math(t):
    t = convert_word_fractions(t)
    t = text2num(t)
    return t    
    
if __name__ == "__main__":
    text2num_test()
    convert_word_fractions_test()
    replace_whole_words_test()