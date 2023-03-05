import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score

data = pd.read_csv('./data/emails.csv', sep=',', encoding='cp1252')

# X => features
X = data['email_text']
# y => target class
y = data['class']

# perform 80/20 split on the dataset for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
