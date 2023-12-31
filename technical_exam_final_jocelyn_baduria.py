# -*- coding: utf-8 -*-
"""Technical_Exam_Final_Jocelyn_Baduria.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/jocelynbaduria/Technical-Exam/blob/main/Technical_Exam_Final_Jocelyn_Baduria.ipynb
"""

!pip install datatable

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datatable as dt

# Scaling the Dataset
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import sklearn.metrics as metrics
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score

from sklearn.metrics import confusion_matrix, accuracy_score, ConfusionMatrixDisplay
from sklearn.metrics import classification_report

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB

from sklearn.feature_extraction.text import TfidfVectorizer

DT = dt.fread('/content/drive/MyDrive/Technical Exam - Senior AI Machine Learning Engineer (2).zip (Unzipped Files)/sentiment_test_cases_1.csv')

#Convert the csv file into pandas dataframe
DT.head()

data_pd = DT.to_pandas()

data_pd.head()

"""Swap the columns text and expected_sentiment"""

column_names = ['text', 'expected_sentiment']

data_pd = data_pd.reindex(columns=column_names)

"""Check if columns are swapped"""

print(data_pd)

# Save the dataframe to a CSV file
data_pd.to_csv('/content/drive/MyDrive/Technical Exam - Senior AI Machine Learning Engineer (2).zip (Unzipped Files)/sentiment_test_cases.csv', index=False)

print(data_pd['expected_sentiment'])

print(data_pd['text'])

"""Cleaning the text for preparation of sentiment analysis"""

# Stop words is a list of really common words, like articles, pronouns, prepositions, and conjunctions
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []

# We need to keep the word not in a sentence to know when a statement is being negated.
for i in range(0, 498):
  review = re.sub('[^a-zA-Z]', ' ', data_pd['text'][i])
  review = review.lower()
  review = review.split()
  ps = PorterStemmer()
  all_stopwords = stopwords.words('english')
  all_stopwords.remove('not')
  review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
  review = ' '.join(review)
  corpus.append(review)

print(corpus[0:5])

"""Countvectorizing to encode text into vectors for training the model and creating Bag of Words"""

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 498)
X_transform = cv.fit_transform(corpus).toarray()
y_transform = data_pd.iloc[:, -1].values

"""Converted text into numerical vectors embedding"""

print(X_transform)

print(X_transform.shape)
print(y_transform.shape)

"""### Splitting the Dataset into Training and test set. Perform Model training of different models to compare each model classifier accuracy. Gradient Boosting Classifier achieves the highest performance 68% accuracy. Models trained will not provide accurate results because of lowest accuracy below 80%.

"""

from sklearn.model_selection import train_test_split
import time

scaler = StandardScaler()
X_1 = scaler.fit_transform(X_transform)

X_train, X_test, y_train, y_test = train_test_split(X_1, y_transform, test_size = 0.20, random_state=0)

#second error need to convert column vector y to an 1D array as expected for training one feature
# y_train = y_train.values.ravel()

names = ["Gaussian Naive Bayes","Decision Tree", "MLP Neural Net", "RandomForestClassifier", "GradientBoostingClassifier"]

classifiers = [
    GaussianNB(var_smoothing=1e-09),
    DecisionTreeClassifier(max_depth=5),
    MLPClassifier(solver='adam',alpha=1, max_iter=1000),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    GradientBoostingClassifier(loss='deviance', learning_rate=0.1, n_estimators=100)
    ]
output = pd.DataFrame(columns=['classifier','f1-score', 'precision', 'recall', 'accuracy'])

max_score = 0.0
max_class = ''
# iterate over classifiers

for name, clf in zip(names, classifiers):

    start_time = time.process_time()
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)

    score = (clf.score(X_test, y_test))*100

    precision = np.round(metrics.precision_score(y_test, y_predict, average='macro'),2)
    recall = np.round(metrics.recall_score(y_test, y_predict, average='macro'),2)
    f1 = np.round(metrics.f1_score(y_test, y_predict, average='macro'),2)

    output = output.append({'classifier': name,'f1-score':f1, 'precision':precision,'recall':recall,'accuracy':score}, ignore_index=True)

    if score > max_score:
        clf_best = clf
        max_score = score
        max_class = name

print(80*'-' )
print('Best --> Classifier = %s, Score (test, accuracy) = %.2f' %(max_class, max_score))
display(output)

"""### Predicting the Test set results using unseen sample X_test and y_test

"""

model_prediction = clf.predict(X_test)
print(np.concatenate((y_test.reshape(len(y_test),1),model_prediction.reshape(len(model_prediction),1)),1))

print(model_prediction)

"""### Confusion Matrix for the Best Model Classifier for Sentiment Analysis - Gradient Boosting Classifier. Use this best model for Sentiment Analysis."""

from sklearn.metrics import confusion_matrix, accuracy_score, ConfusionMatrixDisplay, f1_score
from sklearn.metrics import classification_report

labels = ["Positive", "Neutral", "Negative"]
cm = confusion_matrix(y_test, model_prediction)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = labels)
disp.plot()

accuracy = (accuracy_score(y_test, model_prediction))*100

f1 = f1_score(model_prediction, y_test, average="weighted")
print("Accuracy: %.2f" % accuracy)
print("F1 Score:", f1)
print(classification_report(y_test, model_prediction))

"""Model Evaluation using Test Data"""

print("Actual Value:", (y_test[0]))
print("Predicted Value:", model_prediction[0])

print("Actual Value:", y_test[2])
print("Predicted Value:", model_prediction[0])

"""# 1. Model Evaluation Using Input New Data"""

my_sentence = input('')
print((my_sentence, model_prediction[0], "Confidence_Score: %.2f" % accuracy))

my_sentence = "I love you"
print((my_sentence, model_prediction[0], "Confidence_Score: %.2f" % accuracy))

my_sentence = "Thats kind of annoying!"
print((my_sentence, model_prediction[0], "Confidence_Score: %.2f" % accuracy))

my_sentence = "I hate spicy foods"
print((my_sentence, model_prediction[0], "Confidence_Score: %.2f" % accuracy))

"""## 2. Save the model prediction with output CSV data with ff. columns: text, expected_sentiment, model_output, confidence_score

Load the sentiment_test_cases.csv
"""

df = pd.read_csv('/content/drive/MyDrive/Technical Exam - Senior AI Machine Learning Engineer (2).zip (Unzipped Files)/sentiment_test_cases.csv')

df.head(498)

X = df['text']

print(X)

y = df['expected_sentiment']

print(y)

df = {'text':[X], 'expected_sentiment':[y], 'model_output':[model_prediction], 'confidence_score':[accuracy]}

df

saved_model_with_prediction = pd.DataFrame(df)

saved_model_with_prediction.head()

# Todo process each row of csv files and make prediction using saved model prediction
#def process_row(row):
  #return f"text:{row['text']}, expected_sentiment: {row['expected_sentiment']}, model_output: {row['model_prediction']}, confidence_score: {row['accuracy']}"

#saved_model_with_prediction = df.apply(lambda row: process_row(row), axis=1)

saved_model_with_prediction= pd.DataFrame(saved_model_with_prediction, columns=['text','expected_sentiment','model_output','confidence_score']).to_csv('/content/drive/MyDrive/Technical Exam - Senior AI Machine Learning Engineer (2).zip (Unzipped Files)/output_sentiment_test.csv', index=False)