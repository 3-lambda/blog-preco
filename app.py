from flask import Flask, render_template, jsonify, request, json
from validate_email import validate_email
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__, static_url_path='/static')

client = MongoClient('localhost:27017')
db = client.gama_db

@app.route('/', methods=['GET'])
def mostrarPosts():
	posts = get_posts()
	clientes = get_clientes()
	return render_template('index.html', posts=posts, clientes=clientes)

@app.route('/leads')
def mostrarClientes():
	clientes = get_clientes()
	return render_template('leads.html', clientes=clientes)

@app.route('/editor')
def mostrarEditor():
	return render_template('editor.html')

@app.route('/get_posts', methods=['GET'])
def get_posts():
	try:
		posts_db = db.posts.find()
		posts_list = []
		for post in posts_db:
			posts_list.append({
					'titulo': post['titulo'],
					'conteudo': post['conteudo'],
					# 'data_de_publicacao': post['data_de_publicacao'],
					'autor': post['autor']
			})
	except Exception, e:
		return jsonify(status='error', message=str(e))
	return json.dumps(posts_list)

@app.route('/insert_cliente', methods=['POST'])
def insert_cliente():
	json_data = request.json['form']
	is_valid = validate_email(json_data['email'])

	def is_registered(clientes):
		if json_data['email'] in clientes:
				return False
		return True

	clientes = get_clientes()
	if (is_valid and len(json_data['email']) >= 5 and
	len(json_data['nome']) >= 3 and is_registered(clientes)):
		try:
			json_data = request.json['form']
			nome = json_data['nome']
			email = json_data['email']
			pessoa_id = db.clientes.insert_one({
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
		pessoa_id = db.posts.insert_one({
			'conteudo': conteudo, 'titulo': titulo, 'autor': autor, 'data_de_publicacao': datetime.utcnow()
			})
		return jsonify(status='ok', message='Inserido corretamente')
	except Exception, e:
		return jsonify(status='error', message=str(e))

@app.route('/get_clientes', methods=['GET'])
def get_clientes():
	try:
		clientes_db = db.clientes.find()
		clientes_list = []
		for cliente in clientes_db:
			clientes_list.append({
					'nome': cliente['nome'],
					'email': cliente['email'],
					'data': cliente['data'],
					'ip': cliente['ip']
			})
	except Exception, e:
		return jsonify(status='error', message=str(e))
	return json.dumps(clientes_list)


if __name__ == "__main__":
	app.run(host= '0.0.0.0', debug=True)
