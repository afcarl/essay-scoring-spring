import re
import string


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
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90
}

def replaces_text_numbers(text):
    for p,r in SMALL_NUMBERS.items():
	p = p.upper()
	r = str(r)
        text = text.replace(" %s " % (p)," %s " % (r))
    return text
    
def evaluate_expressions(text):
    matches = re.findall("([0-9][\.0-9+-/*() ]+[0-9])",text)
    matches.sort(key=lambda t: -len(t))
    for p in matches:
        try:
            text = text.replace(p,str(eval(p)))
        except:
            pass
    return text

def check_equalities(text):
    correct = 0
    incorrect = 0
    features = {"correct_equations":0, "incorrect_equations":0}
    for l,r in re.findall("([0-9\.]+)=([0-9\.]+)",text):
        if l.endswith("."): l = l[:-1]
        if r.endswith("."): r = r[:-1]
        if float(l)==float(r):
            features["correct_equations"] += 1
        else:
            features["incorrect_equations"] += 1
            
    for l,r in re.findall("([0-9\.]+)!=([0-9\.]+)",text):
        if l.endswith("."): l = l[:-1]
        if r.endswith("."): r = r[:-1]
        if float(l)==float(r):
            features["correct_equations"] += 1
        else:
            features["incorrect_equations"] += 1
    return features
            
def split_math_expressions(text):
    text = re.sub('([0-9]) ([0-9])', '\g<1> | \g<2>', text)
    return text    
    
def simplify_math(text,debug=False,evaluate=True):
    if debug:
        print text
    text = str(text).upper()
    if debug:
        print text
    text = text.replace("\\",'/')
    if debug:
        print text
    text = replaces_text_numbers(text)
    if debug:
        print text
    text = re.sub('([\s])+', ' ', text)
    if debug:
        print text
    
    text = split_math_expressions(text)

    if debug:
        print text    
    text = separate_numbers_and_letters(text)
    # replaces 1.8C with 1.8
    
    # replace and between expressions by &    
    #m  = re.findall("([0-9][\.0-9+-/*()= ]+[0-9]) AND ([0-9][\.0-9+-/*()= ]+[0-9])",text)
    #if len(m) > 0 and len(m[0])==2:
    #    text = text.replace("%s AND %s" % m[0],"%s & %s" % m[0])
    #    if debug:
    #        print "AND divider", m[0]

    # removes spaces
    for p, r in [
         ("([0-9])[cC]","\g<1>")
        ,("([0-9]+)[ ]{0,}\+[ ]{0,}([0-9]+)","\g<1>+\g<2>")
        ,("([0-9]+)[\s]?=[\s]?([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+)[\s]?-[\s]?([0-9]+)","\g<1>-\g<2>")
        ,("([0-9]+)[\s]?\*[\s]?([0-9]+)","\g<1>*\g<2>")
        ,("([0-9]+)[\s]?/[\s]?([0-9]+)","\g<1>/\g<2>")
        
        # 
        ,("([0-9]+) IS * BY ([0-9]+)","\g<1>*\g<2>")
        ,("([0-9]+) IS MULTIPLIED BY ([0-9]+)","\g<1>*\g<2>")
        ,("([0-9]+) MULTIPLIED ([0-9]+)","\g<1>*\g<2>")
        ,("([0-9]+) MULTIPLIED BY ([0-9]+)","\g<1>*\g<2>")        
        ,("([0-9]+) TIMES ([0-9]+)","\g<1>*\g<2>")
        ,("([0-9]+) X ([0-9]+)","\g<1>*\g<2>")
        ,("([0-9]+) MULTIPLY BY ([0-9]+)","\g<1>*\g<2>")
        ,("([0-9]+) ADD ([0-9]+)","\g<1>+\g<2>")        
        ,("([0-9]+) AD ([0-9]+)","\g<1>+\g<2>")        
        ,("([0-9]+) AN ([0-9]+)","\g<1>+\g<2>")         
        ,("([0-9]+) PLUS ([0-9]+)","\g<1>+\g<2>")
        ,("([0-9]+) MINUS ([0-9]+)","\g<1>-\g<2>")
        ,("([0-9]+) OVER ([0-9]+)","\g<1>/\g<2>")
        ,("([0-9]+) DIVIDED BY ([0-9]+)","\g<1>/\g<2>")
        ,("([0-9]+) DIVIED BY ([0-9]+)","\g<1>/\g<2>")
        ,("([0-9]+) BY ([0-9]+)","\g<1>/\g<2>")        
        
        ,("1/2 OF ([0-9]+)","0.5*\g<1>")
        ,("1/3 OF ([0-9]+)","0.33333333*\g<1>")
        ,("1/4 OF ([0-9]+)","0.25*\g<1>")
        ,("1/5 OF ([0-9]+)","0.20*\g<1>")
        
        # equality    
        ,("([0-9]+) IS ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) EQUALS ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) EQUALS TO ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) EQUALS THE SAME AS THE FRACTION ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS EQUALED TO ([0-9]+)","\g<1>=\g<2>")  
        ,("([0-9]+) ROWS OF ([0-9]+)","\g<1>=\g<2>")  
        ,("([0-9]+) IS ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IT IS ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS JUST ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS EQUAL TO ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS EQUIVALENT TO ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS = TO ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) CAN ALSO TURN TO ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) CAN TURN TO ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS A DECIMAL FOR ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IN DECIMAL FORM IS ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS THE DECIMAL FOR ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS THE SAME AS ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS THE SAME AS THE FRACTION ([0-9]+)","\g<1>=\g<2>")
        ,("([0-9]+) IS THE ANSWER TO ([0-9]+)","\g<1>=\g<2>")
        
        # inequality    
        ,("([0-9]+) IS NOT THE SAME AS ([0-9]+)","\g<1>!=\g<2>")
        ,("([0-9]+) IS A FRACTION FOR ([0-9]+)","\g<1>!=\g<2>")
        ,("([0-9]+) IS NOT A FORM ([0-9]+)","\g<1>!=\g<2>")
        ,("([0-9]+) IS NOT EQUIVALENT TO ([0-9]+)","\g<1>!=\g<2>")
        
        # < > 
        ,("([0-9]+) IS BIGGER THAN ([0-9]+)","\g<1>>\g<2>")
        ,("([0-9]+) IS BIGER THAN ([0-9]+)","\g<1>>\g<2>")
        
        ]:
        text = re.sub(p, r, text)

    text = split_math_expressions(text)

    if evaluate:
        text = evaluate_expressions(text)
        
    if debug:
        print text
    
    return text
    
def get_math_expressions_features(text):
    text = simplify_math(text)
    features = check_equalities(text)
    return features

def remove_multiple_spaces(text):
    return re.sub("([\s]+)"," ",text)

def separate_numbers_and_letters(text):
    text = re.sub("([^0-9])([0-9])","\g<1> \g<2>",text)
    text = re.sub("([0-9])([^0-9])","\g<1> \g<2>",text)   
    text = remove_multiple_spaces(text)
    return text

def leave_only_math_expressions(text):
    text = simplify_math(text,evaluate=False)
    expr = re.findall("([^\.0-9+-/*()= ]+)",text)
    for m in sorted(expr,key=lambda t: -len(t)):
        text = text.replace(m,"|")
    text = separate_numbers_and_letters(text)
    while text.find("| |") >= 0:
        text = text.replace("| |","|")
    return text

if __name__ == "__main__":
    #print simplify_math("2 PLUS 2 EQUALS 4")
    #print simplify_math("2/2 PLUS 1 EQUALS 2")
    #print simplify_math("2 TIMES 2 PLUS 2 EQUALS 7")
    #print "6 + (6 + 6) = 18", simplify_math("6 + (6 + 6) = 18")
    #print simplify_math("NO BECAUSE 6 AN 6 = 12 IN ADDITRON",debug=True)
    #print simplify_math("6 + 6 = 12 AND 9 + 9 = 18",debug=True)
    print check_equalities(simplify_math("<p>1. 18+12=36So 36 wold be the anser",debug=True))
    print simplify_math("THE SUME IS 35 2 35 - 0 = 35")
    #print simplify_math("HE'S CORRECT FOR THE TURKEY BUT NOT THE HAM 2 + 2 + 2 + 2 + 2 + 2 = 16 NOT 18 AND 3 + 3 + 3 + 3 + 3 + 3 = 18 SO ITS CORRECT",debug=True)
    #print leave_only_math_expressions("HE'S CORRECT FOR THE TURKEY BUT NOT THE HAM 2 + 2 + 2 + 2 + 2 + 2 = 16 NOT 18 AND 3 + 3 + 3 + 3 + 3 + 3 = 18 SO ITS CORRECT")    
    #print "0.5 + 0.5 = 1", simplify_math("0.5 + 0.5 = 1.0")
    #print simplify_math("<p>Carmen is right beacause 2x3 is 6 and 1x6 is 6 so they are the same length.</p>")
    #print simplify_math("<p>Number of turkey slices needed: 18</p> <p>Number of ham slices needed: 12</p>  <br>6 x 3 = 18 <br>6 x 2 = 12 <br>Turkey sandwiches: 6  <br>Ham sandwiches: 6    <p>&nbsp;</p> <p>&nbsp;</p> <p>&nbsp;</p> <p>&nbsp;</p> <p>Nick is incorrect because 18 slices of ham is to much ham for ham sandwiches.&nbsp; Ham sandwiches only need 2 slices of ham each.</p> <p>&nbsp;</p>")

    
