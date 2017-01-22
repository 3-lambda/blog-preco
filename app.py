from validate_email import validate_email
from datetime import datetime
from bson.json_util import dumps
from flask import Flask, render_template, redirect, url_for, request, jsonify, json
from urlparse import urlparse, urljoin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
db = SQLAlchemy(app)

class Leads(db.Model):
   id = db.Column('lead_id', db.Integer, primary_key = True)
   nome = db.Column(db.String(100))
   email = db.Column(db.String(200))
   data = db.Column(db.String(200))
   ip = db.Column(db.Integer)

class Posts(db.Model):
   id = db.Column('pead_id', db.Integer, primary_key = True)
   titulo = db.Column(db.String(100))
   conteudo = db.Column(db.String(500))
   autor = db.Column(db.String(100))
   data = db.Column(db.String(200))


def __init__(self, name, city, addr,pin):
   self.nome = nome
   self.email = email

db.create_all()

@app.route('/', methods=['GET'])
def mostrarPosts():
	posts = Posts.query.all()
	return render_template('index.html', posts=posts)

@app.route('/leads')
def mostrarLeads():
	leads = Leads.query.all()
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
		posts_db = Posts.query.all()
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

	leads = Leads.query.all()
	if (is_valid and len(json_data['email']) >= 5 and
	len(json_data['nome']) >= 3 and is_registered(leads)):
		try:
			json_data = request.json['form']
			nome = json_data['nome']
			email = json_data['email']
			leads = Leads(nome, email, datetime.utcnow(), request.remote_addr)
			db.session.add(leads)
			db.session.commit()
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
		post = Posts(conteudo, titulo, autor, datetime.utcnow())
		db.session.add(post)
		db.session.commit()
		return jsonify(status='ok', message='Inserido corretamente')
	except Exception, e:
		return jsonify(status='error', message=str(e))

@app.route('/get_leads', methods=['GET'])
def get_leads():
	try:
		leads_db = Leads.query.all()
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
