from validate_email import validate_email
from pymongo import MongoClient
from datetime import datetime
from bson.json_util import dumps
from flask import Flask, render_template, redirect, url_for, request, jsonify, json
from urlparse import urlparse, urljoin
from flask import request, url_for, redirect

app = Flask(__name__, static_url_path='/static')
ADMIN_PASSWORD = 'gama'
client = MongoClient('localhost:27017')
db = client.gama_db

@app.route('/', methods=['GET'])
def mostrarPosts():
	posts = json.loads(get_posts())
	return render_template('index.html', posts=posts)

@app.route('/leads')
def leads():
	leads = get_leads()
	return render_template('leads.html', leads=leads)

@app.route('/editor')
def editor():
	return render_template('editor.html')

@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
	try:
		post = get_posts()
		post = json.loads(post)[int(post_id)]
	except Exception, e:
		return jsonify(status='error', message=str(e))
	return render_template('post.html', post=post)

@app.route('/get_posts', methods=['GET'])
def get_posts():
	try:
		posts_db = db.posts.find()
		posts_list = []
		for post in posts_db:
			posts_list.append({
					'titulo': post['titulo'],
					'conteudo': post['conteudo'],
					'data_de_publicacao': post['data_de_publicacao'],
					'autor': post['autor']
			})
	except Exception, e:
		return jsonify(status='error', message=str(e))
	return json.dumps(posts_list)

@app.route('/insert_lead', methods=['POST'])
def insert_lead():
	json_data = request.json['form']
	is_valid = validate_email(json_data['email'])

	def is_registered(leads):
		if json_data['email'] in leads:
				return False
		return True

	leads = get_leads()
	if (is_valid and len(json_data['email']) >= 5 and
	len(json_data['nome']) >= 3 and is_registered(leads)):
		try:
			json_data = request.json['form']
			nome = json_data['nome']
			email = json_data['email']
			pessoa_id = db.leads.insert_one({
				'nome': nome, 'email': email, 'data': datetime.utcnow(), 'ip': request.remote_addr
				})
			return jsonify(status='ok', message='Inserido corretamente')
		except Exception, e:
			return jsonify(status='error', message=str(e))
	else:
		return jsonify(status='error', message='Cadastro invalido!')

@app.route('/insert_conteudo', methods=['POST'])
def insert_conteudo():
	json_data = request.json['form']
	try:
		json_data = request.json['form']
		conteudo = json_data['conteudo']
		titulo = json_data['titulo']
		autor = json_data['autor']
		imagem = json_data['imagem']
		pessoa_id = db.posts.insert_one({
			'conteudo': conteudo, 'titulo': titulo, 'autor': autor, 'data_de_publicacao': datetime.utcnow()
			})
		return jsonify(status='ok', message='Inserido corretamente')
	except Exception, e:
		return jsonify(status='error', message=str(e))

@app.route('/get_leads', methods=['GET'])
def get_leads():
	try:
		leads_db = db.leads.find()
		leads_list = []
		for lead in leads_db:
			leads_list.append({
					'nome': lead['nome'],
					'email': lead['email'],
					'data': lead['data'],
					'ip': lead['ip']
			})
	except Exception, e:
		return jsonify(status='error', message=str(e))
	return json.dumps(leads_list)


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] != 'admin' or request.form['password'] != '123':
        error = 'Credenciais Invalidas! Tente novamente'
    else:
        return redirect(url_for('editor'))

if __name__ == "__main__":
	app.run(host= '0.0.0.0', debug=True)
