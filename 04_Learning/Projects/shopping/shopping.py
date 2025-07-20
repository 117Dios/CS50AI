import csv
import sys
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    
    months = {
    "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3,
    "May": 4, "Jun": 5, "Jul": 6, "Aug": 7,
    "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11,
    "June": 5, "Sept": 8  # add any variants your CSV has
    }   
    
    try:
        with open(filename, mode="r") as file:
            fcsv = csv.DictReader(file)# To skip headers
            
            keys = fcsv.fieldnames

            for row in fcsv:
                row_list = []
                
                for key in keys:
                    
                    # If the key is one of these, transform the value in int
                    if key in ["Administrative","Informational","ProductRelated", "OperatingSystems","Browser","Region", "TrafficType"]:
                        row[key] = int(row[key])
                    
                    # If the key is in one of these, transform them into floats
                    if key in ["Administrative_Duration","Informational_Duration","ProductRelated_Duration","BounceRates","ExitRates","PageValues","SpecialDay"]:
                        row[key] = float(row[key])
                        
                    # If the key is the month, turn it into a number and subtract 1 to stay in interval {0, 11}
                    elif key == "Month":
                        row[key] = months[row[key]]
                        
                    # If it's Weekend, transform True in 1 and False in 0
                    elif key in ["Weekend", "Revenue"]:
                        if row[key] == "TRUE":
                            row[key] = 1
                        else:
                            row[key] = 0
                            
                    # Transform Returning visitors in 1 and new visitors in 0
                    elif key == "VisitorType":
                        if row[key] == "Returning_Visitor":
                            row[key] = 1
                        else:
                            row[key] = 0
                    
                    
                    row_list.append(row[key])
            
                evidence.append(row_list[:-1])
                labels.append(row_list[-1])
    except FileNotFoundError:
        sys.exit("File does not exist")
    
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    true_positives = 0
    true_negatives = 0
    sample_size = len(labels)
    
    for i in range(sample_size):
        if labels[i] == predictions[i]:
            if labels[i] == 1:
                true_positives += 1
            else:
                true_negatives += 1
    
    sensitivity = true_positives / labels.count(1)
    specificity = true_negatives / labels.count(0)
    
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
