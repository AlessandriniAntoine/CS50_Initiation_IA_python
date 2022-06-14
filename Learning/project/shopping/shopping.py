import csv
import sys

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


def month(name):
    """
    return 0 for January, 1 for February, 2 for March, etc. up to 11 for December
    """
    list = ["Jan","Feb","Mar","Apr","May","June","Jul","Aug","Sep","Oct","Nov","Dec"]
    return list.index(name)

def visitortype(value):
    """
    return 1 for returning visitors and 0 for non-returning visitors
    """
    return 1 if value == "Returning_Visitor" else 0

def weekend(value):
    """
    return 1 if the user visited on a weekend and 0 otherwise.
    """
    return int(value == "True")

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
        - Month, an index from 0 (January) to (December) 
        - OperatingSystems, an integer 
        - Browser, an integer 
        - Region, an integer 
        - TrafficType, an integer 
        - VisitorType, an integer 0 (not returning) or 1 (returning) 
        - Weekend, an integer 0 (if false) or 1 (if true) 

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) # pass the header
        evidence = []
        labels = []
        for row in reader :
            a = []
            for i in range(3):
                a.extend([int(row[2*i]),float(row[2*i+1])])
            a += [float(cell) for cell in row[6:10]] + [month(row[10])] + [int(cell) for cell in row[11:15]] + [visitortype(row[15]),weekend(row[16])]
            evidence.append(a)
            labels.append(int(row[-1] == "TRUE"))
    return (evidence,labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model.fit(evidence,labels)


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
    positiveTotal,negativeTotal = 0,0
    positive,negative = 0,0
    for i in range(len(labels)) :
        if labels[i] == 1:
            positiveTotal +=1
            if predictions[i] == labels[i]:
                positive +=1
        else :
            negativeTotal +=1
            if predictions[i] == labels[i]:
                negative +=1
    return (positive/positiveTotal,negative/negativeTotal)




if __name__ == "__main__":
    main()

