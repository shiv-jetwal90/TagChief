import flask
from flask import request, render_template, jsonify


documents = dict()
db = dict()
rdoc = dict()


def lookup(word):
	word = word.lower()
	if db.get(word):
		indexlist = db.get(word)[:10]
		newlist = []
		for ind in indexlist:
			newlist.append(rdoc[ind])
		return newlist
	else:
		return None

 
def index(document, ind):
	t = document.split(" ")
	for token in t:
		token = token.lower()
		# if token in stopwords:
		# 	continue
		if documents.get(document):
			ind = documents[document]
		else:
			documents[document] = ind
			rdoc[ind] = document
		if db.get(token):
			if ind in db.get(token):
				pass
			else:
				db[token].append(ind)
		else:
			db[token] = []
			db[token].append(ind)
	
def preprocessing(data):
	data = data.split('  ')
	for i in range(0, len(data)):
		index(data[i], str(i + 1))

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def fun():
	return render_template('index.html')


@app.route('/index', methods=['GET'])
def home():
	preprocessing(request.args.get('paragraph'))
	return "Index created successfully for the given paragraph" 


@app.route('/search', methods=['GET'])
def func():
	data = request.args.get('search')
	return jsonify(lookup(data))


@app.route('/clear', methods =['GET'])
def clear():
	data = request.args.get('clear')
	data = data.lower()
	if data not in db.keys():
		pass
	else:
		db.pop(data)
	return "All documents have been removed for the given word"


if __name__ == '__main__':
    app.run(threaded=True, port=5000)


	
