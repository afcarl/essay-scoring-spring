from string import lower, printable, upper, letters
from itertools import product
import re

"""
SAFE TRANSFORMATIONS - shouldn't affect the score
"""

CONTRACTIONS = """
aren't	are not
can't	cannot
couldn't	could not
didn't	did not
doesn't	does not
don't	do not
hadn't	had not
hasn't	has not
haven't	have not
he'd	he had; he would
he'll	he will
he's	he is
I'd	I I would
I'll	I will
I'm	I am
I've	I have
isn't	is not
it's	it is
let's	let us
mightn't	might not
mustn't	must not
shan't	shall not
she'd	she had
she'll	she will
she's	she is
shouldn't	should not
that's	that is
there's	there is
they'd	they had
they'll	they will
they're	they are
they've	they have
we'd	we had; we would
we're	we are
we've	we have
weren't	were not
what'll	what will
what're	what are
what's	what is
what've	what have
where's	where is
who'd	who had
who'll	who will
who're	who are
who's	who is
who've	who have
won't	will not
wouldn't	would not
you'd	you had
you'll	you will
you're	you are
you've	you have
"""
CONTRACTIONS = map(lambda x: x.upper().split("\t"),CONTRACTIONS.split("\n"))
CONTRACTIONS = filter(lambda x: len(x) == 2, CONTRACTIONS)
CONTRACTIONS = dict(CONTRACTIONS)

def expand_contractions(text):
    return " ".join([CONTRACTIONS.get(w,w) for w in text.split()])

# separates letters and digits with a space
def separate_numbers_and_letters(text):
    text = re.sub("([^0-9])([0-9])","\g<1> \g<2>",text)
    text = re.sub("([0-9])([^0-9])","\g<1> \g<2>",text)   
    text = remove_multiple_spaces(text)
    return text
    
def separate_numbers_and_letters_test():
    cases = [("Stanley is correct because 2/4 is 1 more than2/3","Stanley is correct because 2 / 4 is 1 more than 2 / 3")
            ,("This0is0text","This 0 is 0 text")
            ,("9A","9 A")
            ,("A9","A 9")
            ,("99","99")]
    
    for a,b in cases:
        #print separate_numbers_and_letters(a), b
        assert separate_numbers_and_letters(a)==b
     
def remove_multiple_spaces(text):
    return re.sub("([\s]+)"," ",text)

def remove_multiple_spaces_test():
    cases = [("yes  it's greater because it is","yes it's greater because it is")
            ,("yes       it's greater because it is","yes it's greater because it is")
            ,("A B  C   D     E      F","A B C D E F")]
    
    for a,b in cases:
        assert remove_multiple_spaces(a)==b
    
def remove_all_non_printable(text):
    return "".join([k for k in text if k in printable])
    
def convert_to_upper(text):
    return text.upper()
    
def replace_consecutive_letters(text):
    for letter in letters:
        text = re.sub("[%s]+" % (letter), letter, text)
    return text

def replace_consecutive_letters_test():
    cases = [("BETTER","BETER")
            ,("AAABBBCCC","ABC")
            ,("ABCA","ABCA")]
    
    for a,b in cases:
        assert replace_consecutive_letters(a)==b
    
def replace_3_or_more_consecutive_letters(text):
    for letter in letters:
        text = re.sub("[%s]{3,}" % (letter), letter + letter, text)
    return text
    
def replace_consecutive_letters_test():
    cases = [("BETTTER","BETTER")
            ,("NOOOOOOOOOO","NOO")]
    
    for a,b in cases:
        assert replace_3_or_more_consecutive_letters(a)==b

def remove_html_tags(text):
    text = re.sub("<[^>]+?>"," ",text)

    text = text.replace("&nbsp;"," ")
    text = text.replace("&NBSP;"," ")    
    text = text.replace("&nbsp"," ")
    text = text.replace("&NBSP"," ")    
    text = text.replace("&quot;"," ")
    text = text.replace("&QUOT;"," ")    
    text = text.replace("&quot"," ")
    text = text.replace("&QUOT"," ")    

    return remove_multiple_spaces(text.strip())
    
def remove_html_tags_test():
    assert remove_html_tags("")==""
    assert remove_html_tags("<P>This is some text</P>")=="This is some text"
    assert remove_html_tags("<p>This is some text</p>")=="This is some text"
    assert remove_html_tags("<a src='abc'>This is some text</a>")=="This is some text"
    assert remove_html_tags("<a <b>This is some text</a>")=="This is some text"

# function that cleans the text in a safest possible way that do not changes the text too much
# just necessary standarization
def safe_clean_text(text):
    text = str(text)
    text = text.upper().strip()
    text = expand_contractions(text)
    text = separate_numbers_and_letters(text)
    text = remove_all_non_printable(text)
    for repl in [",",".","!","?"]:
        text = text.replace(repl," ")
    text = text.replace("\\","/")
    text = remove_multiple_spaces(text)
    text = replace_3_or_more_consecutive_letters(text)
    text = remove_html_tags(text)
    return text    

def functions_product(text,functions):
    for f in functions:
        text = f(text)
    return text
     
if __name__ == "__main__":
    separate_numbers_and_letters_test()
    remove_multiple_spaces_test()        
    replace_consecutive_letters_test()
    remove_html_tags_test()
    
    print safe_clean_text("<p>Nick is right because for a ham sandwich you need 2 slices. Also for a a turkey sandwich you need 3 slices.&nbsp; 3,6,9,12,15,18 and 2,4,6,8,10,12,14,16,18, that's why Nick is right</p> <p>&nbsp;</p>")
    print safe_clean_text("<p><u><b><b>??????</b></b></u>No becase if he has to make 6 &nbsp;")   
    print safe_clean_text("<p>???<b>no</b><u> </u><b>because if he was&nbsp")