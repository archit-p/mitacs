from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from gensim.test.utils import get_tmpfile
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
import argparse
import joblib
from dask.distributed import Client
import os

def process_csv(csv_filename):
    '''
    wrapper function to read and pre-process a csv file
    utilizes pandas
    '''
    import pandas as pd

    df = pd.read_csv(csv_filename)

    df[df.isnull().any(axis=1)]
    df.drop(df[df.isnull().any(axis=1)].index, inplace=True)

    return df

def train_d2v_model(model, labelled_ngrams, n_epochs):
    '''
    takes Doc2Vec model and labelled sentences as input and returns a trained model
    training takes place for n_epochs (generally 10 or 20 is a good value)
    '''

    model.build_vocab(labelled_ngrams)

    for epoch in range(n_epochs):
        model.train(labelled_ngrams, epochs=model.iter,
                                total_examples=model.corpus_count)
        print("Epoch #{} is complete.".format(epoch+1))

    return model

def save_d2v_model(model, fpath):
    '''
    takes as input a Doc2Vec model and filepath and exports the model to given path
    '''
    from gensim.test.utils import get_tmpfile

    fname = get_tmpfile(fpath)
    model.save(fname)

def load_d2v_model(fpath):
    '''
    takes as input a filepath and loads a model from the given path
    '''
    from gensim.test.utils import get_tmpfile

    fname = get_tmpfile(fpath)
    return Doc2Vec.load(fname)

def save_clf(clf, fpath):
    '''
    takes as input a filepath and saves given classifier to the path
    '''
    import joblib

    joblib.dump(clf, fpath)

def load_clf(fpath):
    '''
    takes as input filepath and loads a classifier from the given path
    '''
    import joblib

    return joblib.load(fpath)

def print_stats(y_pred, y_test):
    '''
    takes as input test array and predicted array and prints some useful stats
    current stats are:
    1. Accuracy
    2. Precision
    3. F1 Score
    '''
    from sklearn import metrics

    print("Accuracy = " + str(metrics.accuracy_score(y_test, y_pred)))
    print("Precision = " + str(metrics.precision_score(y_test, y_pred)))
    print("F1 Score = " + str(metrics.f1_score(y_test, y_pred)))

def main():

    '''
    create a parser to rad the command line arugments
    arguments are returned as an object
    '''
    parser = argparse.ArgumentParser(description="machine learning model")
    parser.add_argument('-c', '--csv_filename', default=None,
            help='filename for the csv dataset')
    parser.add_argument('-d', '--debug', action='store_true',
            help='turn on debug statements')

    args = parser.parse_args()

    if args.csv_filename:
        csv_filename = args.csv_filename
    else:
        parser.print_help()
        exit()
    if args.debug:
        debug = True
    else:
        debug = False

    '''
    open the csv file for processing
    '''
    if debug:
        print("Starting to read CSV")
    df = process_csv(csv_filename)

    if debug:
        print("Read CSV ---> DONE!")

    '''
    obtain the test number from the csv filename
    this is used later for saving model and classifier
    '''
    try:
        test_num = args.csv_filename.rsplit("/")[-1].rsplit("_")[0]
    except:
        test_num = 0

    '''
    perform labelling of given n-grams
    doc2vec requires each document to be labelled
    '''

    if debug:
        print("Starting to process ngrams")
    ngrams = df['ngram']
    labelled_ngrams = []
    for i in range(len(ngrams)):
        labelled_ngrams.append(TaggedDocument(ngrams[i].split(), [i]))

    if debug:
        print("Process ngrams ---> DONE!")
    '''
    create a model and export it to the given path
    '''
    if debug:
        print("Creating model")
    model = Doc2Vec(dm=1, min_count=1, window=10, vector_size=150,
            sample=1e-4, negative=10)
    if debug:
        print("Model --> CREATED!")
    if debug:
        print("Training model")
    trained_model = train_d2v_model(model, labelled_ngrams, n_epochs=20)
    if debug:
        print("Model --> TRAINED!")

    d2v_path = os.path.join(os.get_pwd(), "doc2vec_model{}".format(test_num))
    save_d2v_model(trained_model, d2v_path)

    model_loaded = load_d2v_model(d2v_path)

    '''
    generate the target array
    this is needed as target can only be integers however in our
    case the dataset contains the 'Benign' and 'Malware' tags
    transformation is achieved using the module LabelEncoder from sklearn
    '''
    le = LabelEncoder()
    le.fit(["Benign", "Malware"])
    target = le.transform(df['label'])

    '''
    get the inference vectors from d2v model
    '''
    data = []
    for i in range(len(df['ngram'])):
        data.append(model_loaded[i])

    '''
    create a split for test and training data
    currently its 70% and 30%
    '''
    x_train, x_test, y_train, y_test = train_test_split(data, target,
            test_size=0.3, random_state=0)

    '''
    initialize an SVM classifier and perform fitting for the given training data
    '''

    client = Client(processes=False)

    clf = svm.SVC(kernel='linear')

    with joblib.parallel_backend('dask'):
        clf.fit(x_train, y_train)

    '''
    create a prediction array to later compare with the test array
    '''
    y_pred = clf.predict(x_test)

    '''
    describe the classifer path and then save the classifier
    '''

    clf_path = "/home/architp/projects/def-daknox/architp/mitacs/ml/model{}.pkl".format(test_num)
    save_clf(clf, clf_path)

    '''
    finally print the stats
    '''
    print_stats(y_pred, y_test)

if __name__ == "__main__":
    main()
