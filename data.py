# Inputting sentiment/ words Data
import pandas as pd
import numpy as np
sentiment_score_data = pd.read_csv("afinn.csv", encoding = "ISO-8859-1")
sentiment_score_data_words = np.array(sentiment_score_data.iloc[:,1])[0]
sentiment_score_data_scores = np.array(sentiment_score_data.iloc[:,2])[0]
sentiment_scores_table = pd.DataFrame().from_dict(data={"word": sentiment_score_data_words, "sentiment" : sentiment_score_data_scores}, orient="index")


def nanfunction(value):
    if value == 1 or value == "1":
        return 1
    else:
        return 0

def nanfunction_str(string):
    if type(value) == str:
        return value
    else:
        return 0


def remove_spaces(string):
    string = string.replace(" ", "")
    return string


def cleaning_func(table):
# this function is used to fix the nan values
# in the original csv
# then it removes the 1st row which is the Date
# and prints the Dates name
# and returns the cleaned up table
    names_array = table.column("Unnamed: 0")
    table = table.with_column("Name", names_array).drop("Unnamed: 0").drop("Age")
    new_right = table.apply(nanfunction, "Right")
    new_left = table.apply(nanfunction, "Left")
    new_line = table.apply(nanfunction, "Line")
    new_table = table.with_columns("Right", new_right, "Left", new_left)
    return new_table

def cleaning_func2(table):
    new_line_types = table.apply(remove_spaces, "Line_Type")
    table = table.with_column("Line_Type",new_line_types)
    new_names = table.apply(remove_spaces, "Name")
    table = table.with_column("Name",new_names)
    new_right = table.apply(nanfunction, "Right")
    new_left = table.apply(nanfunction, "Left")
    new_line = table.apply(nanfunction, "Line")
    new_table = table.with_columns("Right", new_right, "Left", new_left)


def change_type(value):
    if value == 1 or value == "1":
        return 1
    else:
        return 0

def remove_spaces(string):
    if string == 0:
        return string
    else:
        string = string.replace(" ", "")
        return string

all_data = pd.read_csv("Sheet 5-All_Data.csv")
all_data = all_data.fillna(0)
all_data["Name"] = all_data["Name"].map(remove_spaces)
all_data["Line_Type"] = all_data["Line_Type"].map(remove_spaces)
all_data["Right"] = all_data["Right"].map(change_type)
all_data["Left"] = all_data["Left"].map(change_type)
# all_data = all_data[all_data["Line"].map(lambda x: type(x) == str)]

original_data = all_data
original_data = original_data.drop(0,axis=0)


# This table contains 1616 bad words.
bad_words = pd.read_csv("bad-words (1).csv", header=None)
bad_words = np.array(bad_words[0])


def bad_words_score(string,weight=200):
    score = 0
    multiple=False
    for word in string.split():
        if word in bad_words and multiple:
            score += 1
            score = score * score
        elif word in bad_words and not multiple:
            score += 1
            multiple=True

    return score * weight


from textblob import TextBlob

def split_len(string):
    return len(string.split())


# Line score assigns a score to a given pickup line
# which is based the sentiment of the pickup line
# I created weights to tweak how import subjectivity is
# vs polarity.
def sentiment(line, weight_1=10, weight_2=100):
    blob_polarity = TextBlob(line).sentiment.polarity * weight_2
    blob_subject = TextBlob(line).sentiment.subjectivity * weight_1
    sentiment_words = sentiment_scores_table["word"]
    score = 0
    line = line.split()
    for L in line:
        if L in sentiment_words:
            score += sentiment_scores_table[sentiment_scores_table["word"] == L]["score"][0]
    return score + blob_polarity + blob_subject


def sentiment_2(line,polarity=True):
    blob1 = TextBlob(line)
    if polarity:
        return blob1.sentiment.polarity
    else:
        return blob1.sentiment.subjectivity


def extract_features(pickup_line):
    bad_words = bad_words_score(pickup_line)
    length = len(pickup_line)
    sentiment = sentiment_2(pickup_line,False)
    subjectivity = sentiment_2(pickup_line,False)
    score = bad_words + subjectivity
    polarity = sentiment_2(pickup_line,True)

    features = ([bad_words,
                 length,
                 sentiment,
                 score,
                 polarity,
                 subjectivity]
               )
    return features





from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing



# keep_list = ["bad_words_score", "polarity", "subjectivity", "Lengths"]
input_table = pd.read_csv("features_pickuplines.csv").drop("Unnamed: 0", axis=1)

scaler = preprocessing.StandardScaler().fit(input_table)
X_scaled = scaler.transform(input_table)

labels_processing = pd.read_csv("pickup_lines_labels.csv")["Label"]


# Model:

import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix


seed = 0
neighbors=13

# x = input_table.drop("labels", axis=1)


def run_KNN(k=neighbors,table=input_table, X_data=X_scaled, Y_data=labels_processing, PCA_on=False, shuffle=True, re_scale=True):
    X = X_scaled

    Y = labels_processing

    # pick training and test data sets
    # I chose to put 80% of the data into the training set, and 20% into the test set.
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = .25, shuffle=shuffle, random_state=seed)


    classifier = KNeighborsClassifier(n_neighbors=k)
    classifier.fit(X_train, Y_train)
    y_pred = classifier.predict(X_test)
    accuracy = sum(y_pred == Y_test) / len(Y_test)
    print("Accuracy is: ")
    print(accuracy)
    return (scaler, classifier)

# run_KNN(100,k = 5, PCA_on=False, shuffle=False, re_scale=True)
classifier = run_KNN(k=neighbors,table=input_table,PCA_on=False, shuffle=True, re_scale=True)[1]



def predict_a_new_line(pickup_line):
    features = np.array(extract_features(pickup_line))
    line = pd.DataFrame(features).T
    print(line)
    X_scaled = scaler.transform(line)
    prediction = classifier.predict(X_scaled)
    return prediction[0]


print(predict_a_new_line("I really love your attention to detail, and think you have a way with words, could I get your number?"))
