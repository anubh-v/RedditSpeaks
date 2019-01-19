from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
import string

# return an array of tokens (with stopwords and punctuation filtered, stemed)
def tokenize(sentence):
    
    MISC_STOPWORDS = ["'s", "http", "https"]
     
    tokens = word_tokenize(sentence)

    tokens = [w.lower() for w in tokens]

    stop_words = list(stopwords.words('english')) + MISC_STOPWORDS
    print(stop_words)
    tokens = [w for w in tokens if not w in stop_words]

    punctSet = list(string.punctuation)
    tokens = [w for w in tokens if not w in punctSet]

    return tokens
