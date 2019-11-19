import flask
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from flask import request, render_template, jsonify
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer 
import redis
conn = redis.Redis('localhost')
tokenizer = nltk.word_tokenize
stemmer = EnglishStemmer()
index = defaultdict(list)
documents = {}
#__unique_id = 0
stopwords = nltk.corpus.stopwords.words('english')

def lookup( word):
	word = word.lower()
	if stemmer:
		word = stemmer.stem(word)
	if conn.get(word):
		return conn.get(word).decode("utf-8")
	else:
		return None

 
def add( document):
	print(document)
	for token in [t.lower() for t in nltk.word_tokenize(document)]:
		#print(token)
		if token in stopwords:
			continue
		if stemmer:
			token = stemmer.stem(token)
		if conn.get(token):
			if document in conn.get(token).decode("utf-8"):
				pass
			else:
				st = conn.get(token).decode("utf-8")+ "\n\n"+ document
				conn.set(token, st)
		else:
			conn.set(token, document)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def fun():
	return render_template('index.html')



@app.route('/index', methods=['GET'])
def home():
	data = request.args.get('paragraph').split('  ')
	for i in data:
		add(i)
	#print(data.split('  '))
	return "index created successfully for these document"


@app.route('/search', methods=['GET'])
def func():
	data = request.args.get('search')
	#print(data.split('  '))
	print(lookup(data))
	return jsonify(lookup(data))


@app.route('/clear', methods =['GET'])

def clear():
	data = request.args.get('clear')
	conn.delete(data)
	return "all indexed has been removed"

app.run()
	
