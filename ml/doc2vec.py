import pandas as pd
import numpy as np
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score
from gensim.test.utils import get_tmpfile
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
from sklearn.externals import joblib
import argparse

parser = argparse.ArgumentParser(description="machine learning model")

parser.add_argument('-c', '--csv_filename', default=None, help='describe the filename of the csv file')

args = parser.parse_args()

print("--> Reading CSV")
df = pd.read_csv(args.csv_filename)

df[df.isnull().any(axis=1)]

df.drop(df[df.isnull().any(axis=1)].index, inplace=True)

ngrams = df['ngram']
labelled_ngrams = []
print("--> Labelling Tuples")
for i in range(len(ngrams)):
    labelled_ngrams.append(TaggedDocument(ngrams[i].split(), [i]))

print("--> Forming model")
#'''
# block to train and save the neural net
model = Doc2Vec(dm=1, min_count=1, window=10, vector_size=150, sample=1e-4, negative=10)

model.build_vocab(labelled_ngrams)

print("--> Training")
for epoch in range(20):
    model.train(labelled_ngrams, epochs=model.iter,
            total_examples=model.corpus_count)
    print("Epoch #{} is complete.".format(epoch+1))
#'''
test_num = args.csv_filename.rsplit("/")[-1].rsplit("_")[0]
fpath = "/home/architp/projects/def-daknox/architp/mitacs/ml/doc2vec_model{}".format(test_num)
fname = get_tmpfile(fpath)
#'''
model.save(fname)
#'''
model_loaded = Doc2Vec.load(fname)
#'''
target = []
for tag in df['label']:
    if(tag == 'Benign'):
        target.append(0)
    elif(tag == 'Malware'):
        target.append(1)

data = []
for i in range(len(df['ngram'])):
    data.append(model_loaded[i])

x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=0)
#'''
#block to create the classifier
clf = svm.SVC(kernel='linear')
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
#'''
#block to save the classifier
clf_fname = "/home/architp/projects/def-daknox/architp/mitacs/ml/model{}.pkl".format(test_num)
#'''
joblib.dump(clf, clf_fname)
#'''
'''
#block to load classifier and then predict
loaded_clf = joblib.load(clf_fname)
y_pred = loaded_clf.predict(x_test)
'''
print("Accuracy = " + str(metrics.accuracy_score(y_test, y_pred)))
print("Precision = " + str(metrics.precision_score(y_test, y_pred)))
print("F1 Score = " + str(metrics.f1_score(y_test, y_pred)))
