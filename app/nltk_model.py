import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier

nltk.download('punkt')
nltk.download('stopwords')

# labeled dataset for training.
training_data = [
    ("Terrorist attack in the city", 'Terrorism'),
    ("Students are protesting against fee hike", 'Protest'),
    ("Shrilanka is facing political unrest after china high debt", 'Political Unrest'),
    ("Amidst uneasy calm in Mira Road, residents blame miscreants for rioting", 'Riot'),
    ("Earthquake shakes the region", 'Natural Disaster'),
    ("Heartwarming story about a rescue", 'Uplifting'),
    ("Economic report on market trends", 'Other'),
]

# Preprocess the data
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return dict([(word, True) for word in words])

# Apply preprocessing to the training data
training_set = [(preprocess_text(text), category) for (text, category) in training_data]

# Train a Naive Bayes classifier
classifier = NaiveBayesClassifier.train(training_set)

# Example of classifying a new text
def categorize(text):
    text_features = preprocess_text(text)
    category = classifier.classify(text_features)
    return category

# Test with sample texts
sample_texts = [
    "There was a terrorist attack in the city",
    "A heartwarming story about kindness and generosity",
    "An earthquake devastated the region",
    "The stock market experienced a downturn",
]

for text in sample_texts:
    category = categorize(text)
    print(f'Text: "{text}" - Category: {category}')
