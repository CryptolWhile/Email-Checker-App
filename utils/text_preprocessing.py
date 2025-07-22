import nltk
import string
import random

nltk.download('punkt')
nltk.download('stopwords')

def lowercase(text): return text.lower()

def punctuation_removal(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def tokenize(text): return nltk.word_tokenize(text)

def remove_stopwords(tokens):
    stop_words = nltk.corpus.stopwords.words('english')
    return [token for token in tokens if token not in stop_words]

def stemming(tokens):
    stemmer = nltk.stem.PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

def handle_negation(text):
    negation_words = ["not", "no", "never", "n't", "cannot"]
    tokens = text.split()
    new_tokens = []
    negating = False
    for word in tokens:
        if word in negation_words:
            negating = True
            new_tokens.append(word)
            continue
        if negating:
            new_tokens.append("NOT_" + word)
            negating = False
        else:
            new_tokens.append(word)
    return ' '.join(new_tokens)

def shuffle_words(tokens):
    shuffled = tokens[:]
    random.shuffle(shuffled)
    return shuffled

def normalize_text(text):
    normalization_dict = {
        "u": "you", "ur": "your", "im": "i am", "m": "i am",
        "dont": "do not", "can't": "cannot", "won't": "will not",
        
    }
    for word, norm in normalization_dict.items():
        text = text.replace(f" {word} ", f" {norm} ")
    return text

def preprocess_text(text):
    text = normalize_text(text)
    text = handle_negation(text)
    text = lowercase(text)
    text = punctuation_removal(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = stemming(tokens)
    tokens = shuffle_words(tokens)
    return ' '.join(tokens)
