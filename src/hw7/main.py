import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# Switch to y-1000.csv for a smaller dataset
DF_NAME = 'y-100000.csv'

# Import DataFrame from CSV
df = pd.read_csv(DF_NAME)

# Set the column names
df = df.set_axis(['s', 'text'], axis=1)

# Get the counts of each sentiment label
sentiment_counts = df['s'].value_counts()

# Create a bar chart with custom x-axis labels
plt.bar(['Negative', 'Positive'], sentiment_counts.values,
        tick_label=['Negative', 'Positive'])

# Add axis labels and title
plt.xlabel('Sentiment Label')
plt.ylabel('Number of Texts')
plt.title('Distribution of Sentiment Labels in Yelp Reviews')

# Display the chart
# plt.show()
plt.savefig("stats.png")
print('Saving chart of input data target class distribution to stats.png')

# Split the test data
X = df['text']
y = df['s']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, train_size=0.9, random_state=1234)

# Perform Multinoial Naive Bayes
print('Performaing Multinomial Naive Bayes...')
mnb_pipe = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('mnb', MultinomialNB())
                     ])
mnb = mnb_pipe.fit(X_train, y_train)
print("\tMultinomial Naive Bayes Accuracy:", accuracy_score(mnb.predict(X_test), y_test))

# Perform Logistic Regression
print('Performaing Logistic Regression...')
lgr_pipe = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', LogisticRegression(n_jobs=1, C=1e5)),
                     ])
lgr = lgr_pipe.fit(X_train, y_train)
print("\tLogistic Regression Accuracy:", accuracy_score(lgr.predict(X_test), y_test))

# Perform MLP Classifier
print('Performaing MLP Classifier...')
mlp_pipe = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('neuralnet', MLPClassifier(solver='lbfgs', alpha=1e-5,
                                hidden_layer_sizes=(15, 7), random_state=1)),
])
mlp = mlp_pipe.fit(X_train, y_train)
print("\tMLP Classifier Accuracy:", accuracy_score(mlp.predict(X_test), y_test))