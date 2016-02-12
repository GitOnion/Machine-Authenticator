import numpy as np
from sklearn import svm
from sklearn import cross_validation
from lib import brainlib


def feature_vector_generator(binned_PS_list):
    '''Average the binned power spectrum.'''
    # holder = []
    # for binned_PS in binned_PS_list:
    #     holder.append(brainlib.avgPowerSpectrum(binned_PS, np.log10))
    return(brainlib.avgPowerSpectrum(binned_PS_list, np.log10))


def labeler(feature_vectors_list):
    '''Takes an list of feature vectoers and produces two lists X and y
    where len(X) = len(y),
    X is the vectors, y is their (numerical) labels.'''
    X = []
    y = []
    currentLabel = 0
    for feature_vector in feature_vectors_list:
        for vector in feature_vector:
            X.append(vector)
            y.append(currentLabel)
        currentLabel += 1
    return(X, y)


def crossValidate(X, y):
    "7-fold cross-validation with an SVM with a set of labels and vectors"
    clf = svm.LinearSVC()
    scores = cross_validation.cross_val_score(clf, np.array(X), y, cv=7)
    return(scores.mean(), scores.std())


def svm_learner(train_data_target, train_data_other):
    '''Takes in two lists of training data, and returns a linear classifier.'''
    Target = feature_vector_generator(train_data_target)
    Other = feature_vector_generator(train_data_other)
    X, y = labeler([Target, Other])
    linear_classifier = svm.LinearSVC()
    linear_classifier.fit(X, y)
    return(linear_classifier)
