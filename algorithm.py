import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pickle

data = pd.read_csv('./data/emails.csv', sep=',', encoding='cp1252')

# X => features
X = data['email_text']
# y => target class
y = data['class']

# perform 80/20 split on the dataset for training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# vectorize
vectorizer = TfidfVectorizer()

# converts text to numbes for performing classification
X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

# uses the C-Support Vector Machine algorithm with linear kernel
classifier = SVC(kernel='linear')
classifier.fit(X_train_vector, y_train)

# get the predicted classes
y_predict = classifier.predict(X_test_vector)

# evaluate model performance
accuracy = accuracy_score(y_test, y_predict)
precision = precision_score(y_test, y_predict, average='weighted')
recall = recall_score(y_test, y_predict, average='weighted')

# Save the trained model and vectorizer
with open('model.pkl', 'wb') as f:
    pickle.dump(classifier, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)


def predict_tag(email):
    # Load the saved mode and vectorizer
    with open('model.pkl', 'rb') as f:
        loaded_classifier = pickle.load(f)

    with open('vectorizer.pkl', 'rb') as f:
        loaded_vectorizer = pickle.load(f)

    # Vectorize the input email
    email_vector = loaded_vectorizer.transform([email])

    # Make the prediction
    predicted_tag = loaded_classifier.predict(email_vector)

    # Return the first (and only) prediction
    return predicted_tag[0]
