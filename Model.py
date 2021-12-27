



import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA

seed = 27
neighbors=3

x = input_table.drop("labels", axis=1)


def run_KNN(loops,k=neighbors,table=input_table, X_data=X_scaled, Y_data=labels_processing, PCA_on=False, shuffle=True, re_scale=True):
    scores = []
    current_best = 0
    for i in range(loops):
        if re_scale:
            # StandardScaler
            # MinMaxScaler
            scaler = preprocessing.StandardScaler().fit(table_for_processing)
            X_scaled = scaler.transform(table_for_processing)
            X_scaled = pd.DataFrame(X_scaled)
            X = X_scaled

        else:
            X = table_for_processing

        Y = labels_processing

        # pick training and test data sets
        # I chose to put 80% of the data into the training set, and 20% into the test set.
        X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = .1, shuffle=shuffle, random_state=seed)

        if PCA_on:
            pca = PCA(n_components=3)

            # STEP 2: Using "fit_transform," fit the model with the training X data and apply the dimensionality reduction on it.
            X_train = pca.fit_transform(X_train)

            # STEP 3: With the same model, apply the dimensionality reduction on the test X data.
            X_test = pca.transform(X_test)

        classifier = KNeighborsClassifier(n_neighbors=k)
        classifier.fit(X_train, Y_train)
        y_pred = classifier.predict(X_test)
        accuracy = sum(y_pred == Y_test) / len(Y_test)
        scores.append(accuracy)
        if accuracy > current_best:
            current_best = accuracy
            print("current_best: " + str(current_best))
    print("Average Accuracy is: ")
    print(np.mean(np.array(scores)))
    return scaler, classifier

# run_KNN(100,k = 5, PCA_on=False, shuffle=False, re_scale=True)
run_KNN(1,k=neighbors,table=input_table,PCA_on=False, shuffle=True, re_scale=True)
