from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
import string


# return an array of tokens (with stopwords and punctuation filtered, stemed)
def tokenize(sentence):
    tokens = word_tokenize(sentence)

    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]

    punctSet = set(string.punctuation)
    tokens = [w for w in tokens if not w in punctSet]
    return tokens
