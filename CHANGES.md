Description of changes vs prior version
================

Structure of the models
----------------

In the prior version I modeled the scores as regression task.
The scores were predicted using ordinal grading system.
The prediction was a real number which was then transformed to a discrete
grade using "grade on a curve" transformation - it means that
I calculated the share of each grade in the all observations in the 
training observations and applied this share to new data.

Previous approach while giving satisfactory results is very biased.
It evaluates the essays using previous distribution of grades.
This can lead to untrue evaluation if the new essays come 
from a different distribution.

For this reason and also because this time models had to predict
the probability of each grade I decided to change the structure
of models. To create a model for n grades I used n independent 
models. Whichever grade had the highest probability it was chosen
as a final grade. It also made blending of the models more obvious.

Choice of the models
----------------

Apart from using sklearn [GradientBoostingClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html) I decided to try:

- a new boosting library [xgboost](https://github.com/tqchen/xgboost)
- deep learning library [nolearn](https://github.com/dnouri/nolearn)

[xgboost](https://github.com/tqchen/xgboost) is a remarkable implementation
of tree boosting algorithm. One reason is the performance. It is unique
because it allows to train trees using many cores.

Data preprocessing
----------------

Math
----------------

This time 50% of the essays were math based. I spent much time trying to 
clean math essays to normalize them in every possible way.

[text to math](lib/math/text_to_math.py)
--------------
```text_to_math``` is a new module to convert any numbers written in English
to a digit representation number.

Some examples of transformations:

1. replaces one -> 1, two -> 2, ...
2. replaces 2 out of 4 -> 2/4
3. replaces thirds -> 1/3, fourths -> 1/4

[Formulas simplifications](lib/math/math_helpers.py)
--------------

After math cleaning it is possible to evaluate math expressions in the 
essay. Counting the number of true expresssions is a powerful feature.

- ```2 PLUS 2 EQUALS 4``` -> ```4=4```
- ```2/2 PLUS 1 EQUALS 2``` -> ```2=2```
- ```2 TIMES 2 PLUS 2 EQUALS 7``` -> ```6=7```
- ```NO BECAUSE 6 AN 6 = 12 IN ADDITRON``` -> ```NO BECAUSE 12=12 IN ADDITRON```
- ```6 + 6 = 12 AND 9 + 9 = 18``` -> ```12=12 AND 18=18```

Pipeline
================

I refactored the code needed to transform the data. [Pipelines](pipelines.py) are
now lists of steps needed to go from the raw essay text to features.

```
simple_pipeline = {
    "name":"simple_pipeline",
    "steps":[
         EssayTextConversion(source="raw",dest="stem",fun=lambda text: " ".join([stemmer(t) for t in text.split()]))
        ,FunctionalTextEssayFeature(feature_name="text_length_1", fun=lambda essay: len(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="text_length_2", fun=lambda essay: len(essay.texts["stem"]))

        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=2)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=3)
    ]
}
```

This simple pipeline creates basically 3 feature sets:

- text length of original essay text
- text length of stemmed essay text
- 1,2,3-grams for stemmed essay text

Each pipeline defined this way can be applied to essay collection. I created 8 different
pipelines which enabled me to test different features.

New features
================

wikipedia n-gram coverage
----------------

I downloaded the precalculated 1,2,3-grams from wikipedia. I used a coverage
of the ngrams in the essay as a feature. For example if all 2-grams in the
essay were seen on wikipedia that is a score 1.0. If all 2-grams are novel
it is a score 0.0. This gives models some valuable information about the
style of the essay.

sentiment analysis
----------------

Using [TextBlob](https://github.com/sloria/TextBlob) library I calculated
additional features like ```sentiment_polarity``` and ```sentiment_subjectivity```.
Both features turned out to be quite useful.

character based n-grams
----------------

Apart from standard word-based ngrams. I decided to add character based
n-grams (from 1 up to 4-grams in some pipelines). This proved to be very
valuable transformation.

language probability
----------------

To recognized texts written in different languages I used a Python library
(lang.id)[https://github.com/saffsd/langid.py]. I calculated the probability
of the language being English, French and Spanish.

word2vec clusters
----------------

[word2vec](https://code.google.com/p/word2vec/) is a powerful library
to calculate word embeddings. Each word is represented as a vector 
of n real numbers. 

I used precomputed vectors from news articles. A quote from the ```https://code.google.com/p/word2vec/```:

```
We are publishing pre-trained vectors trained on part of Google News dataset (about 100 billion words). The model contains 300-dimensional vectors for 3 million words and phrases.
```

I decided to cluster semantically similar words into clusters. The number
of clusters was chosen to be d / 4. Where d is the number of unique words
in the essay dictionary (bag of words). The reason for this was to 
force to group sparse features into more dense representation.

Model ensemble
================

I generated 107 different model types and parameters.
For the most difficult essays I generated additional models.
Altogether there were 2219 models. The cross validation result
is in the file [results.csv](results.csv).

To merge the results of the models I tried direct optimization of the
weighted kappa metric. Unfortunately this resulted in very poor generalization.
The coefficients began to overfit to the training data. I decided to limit 
its learning potential by using this regularization procedure:

```
repeat 40 times
     sample 50% of the training observations
     optimize weighted kappa on the sample
     save coefficients
calculate average coefficients for each model
```

This resulted in better generalization.