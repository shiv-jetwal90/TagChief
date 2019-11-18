import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer 
 
class Index:

 
    def __init__(self, tokenizer, stemmer=None, stopwords=None):

        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        if not stopwords:
            self.stopwords = set()
        else:
            self.stopwords = set(stopwords)
 
    def lookup(self, word):
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)
        return [id for id in self.index.get(word)]
 
    def add(self, document):
        for token in [t.lower() for t in nltk.word_tokenize(document)]:
            if token in self.stopwords:
                continue
 
            if self.stemmer:
                token = self.stemmer.stem(token)
 
            if self.__unique_id not in self.index[token]:
                self.index[token].append(self.__unique_id)
 
        self.documents[self.__unique_id] = document
        self.__unique_id += 1           
 
 
index = Index(nltk.word_tokenize, 
              EnglishStemmer(), 
              nltk.corpus.stopwords.words('english'))
for i in (["hello how are you", "sumit how ram amit hello"]):
	index.add(i);
print(index.lookup("sumit"))

