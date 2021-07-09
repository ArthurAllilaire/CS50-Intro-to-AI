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
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Miss out the headers
            if row[0] != "Administrative":
                #Row: ['0', '0', '0', '0', '5', '89.5', '0.04', '0.053333333', '0', '0', 'Dec', '1', '1', '3', '2', 'Returning_Visitor', 'TRUE', 'FALSE']
                # Remove label from row and add to label list
                labels.append(0 if row.pop() == 'FALSE' else 1)
                for i in range(len(row)):
                    # For the first ten rows
                    if i < 10:
                        # convert administrative, infromational and product related to ints
                        if i in [0, 2, 4]:
                            row[i] = int(row[i])
                        else:
                            # convert to float
                            row[i] = float(row[i])

                    # Month data column
                    elif i == 10:
                        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                                  'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                        row[i] = int(months.index(row[i]))
                    # For OS, browser, region and traffic type
                    elif i <= 14:
                        # Convert to int
                        row[i] = int(row[i])
                    # For visitor type
                    elif i == 15:
                        row[i] = 1 if row[i] == "Returning_Visitor" else 0

                    # For weekend
                    else:
                        if row[i] == "TRUE":
                            row[i] = 1
                        else:
                            row[i] = 0

                # Add row to evidence
                evidence.append(row)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
