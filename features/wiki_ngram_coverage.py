from __future__ import division
from memoize import memoize
from skipgrams import kskipngrams

import psycopg2
conn = psycopg2.connect("dbname='wiki' user='postgres' host='localhost' port=5432 password='XXXX'")

@memoize
def check_1gram(word):
    cur = conn.cursor()
    cur.execute("select exists(SELECT 1 FROM wp2gram WHERE w1 = '%s')" % (word,))
    return cur.fetchone()[0]

@memoize
def check_2gram(ngram):
    cur = conn.cursor()
    cur.execute("select exists(SELECT 1 FROM wp2gram WHERE w1 = '%s' and w2 = '%s')" % (ngram[0],ngram[1]))
    return cur.fetchone()[0]
    
@memoize
def check_3gram(ngram):
    cur = conn.cursor()
    cur.execute("select exists(SELECT 1 FROM wp3gram WHERE w1 = '%s' and w2 = '%s' and w3 = '%s')" % (ngram[0],ngram[1],ngram[2]))
    return cur.fetchone()[0]

def check_1gram_coverage(text):
    text = text.replace("'"," ")
    ngrams = text.split()
    if ngrams is None or len(ngrams) == 0:
        return 0
    ngrams_covered = [ngram for ngram in ngrams if check_1gram(ngram)]
    if len(ngrams) > 0:
        return len(ngrams_covered) / len(ngrams)
    else:
        return 0

def check_2gram_coverage(text):
    text = text.replace("'"," ")
    ngrams = kskipngrams(text.split(), skip=0, ngram=2)
    if ngrams is None or len(ngrams) == 0:
        return 0

    ngrams_covered = [ngram for ngram in ngrams if check_2gram(tuple(ngram))]
    if len(ngrams) > 0:
        return len(ngrams_covered) / len(ngrams)
    else:
        return 0

def check_3gram_coverage(text):
    text = text.replace("'"," ")
    ngrams = kskipngrams(text.split(), skip=0, ngram=3)
    if ngrams is None or len(ngrams) == 0:
        return 0

    ngrams_covered = [ngram for ngram in ngrams if check_3gram(tuple(ngram))]
    if len(ngrams) > 0:
        return len(ngrams_covered) / len(ngrams)
    else:
        return 0
