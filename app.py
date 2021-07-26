from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import asyncio
import random


app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://<username>:<password>@localhost:5432/<databasename>'
app.secret_key = 'tempseckey'
db = SQLAlchemy(app)
engine = db.engine

from async1 import fetch
from models import User
import flask as fl
import hashing
import json
import auth

PERMISSIONS = ['read', 'update', 'create', 'delete']

"""TASK 1"""


@app.route('/')
def main():
    user = auth.get_user()

    if user is not None:
        return fl.render_template('main.html', users=User.query.all(), current_user=user, permissions=PERMISSIONS)
    return fl.redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if auth.get_user() is not None:
        return fl.redirect('/')
    if fl.request.method == 'GET':
        return fl.render_template('login.html')
    username = fl.request.form['username']
    password = fl.request.form['password']
    user = auth.authenticate(username, password)
    if user is not None:
        auth.login(user)
        return fl.redirect('/')

    return fl.render_template('login.html', error='Not valid login or password')


@app.route('/create', methods=['GET', 'POST'])
def create_user():
    user = auth.get_user()
    if 'create' not in user.user_permissions:
        return fl.render_template('404.html')
    data = fl.request.form
    user_permissions = [perm for perm, v in data.items() if v == 'on']
    u = User(username=data['username'],
             password=data['password'],
             user_permissions=user_permissions,
             is_admin=False)
    db.session.add(u)
    db.session.commit()
    return fl.redirect('/')


@app.post('/update')
def update():
    user = auth.get_user()
    if 'update' not in user.user_permissions:
        return fl.render_template('404.html')
    data = fl.request.form
    user_permissions = [perm for perm, v in data.items() if v == 'on']
    with engine.connect() as con:
        q = con.execute(
            f'update \"User\" set username=\'{data["username"]}\', user_permissions=ARRAY{user_permissions}, password={hashing.hash(data["password"])} where id={data["user_id"]} ')
    return fl.redirect('/')


@app.get('/logout')
def logout():
    fl.session.pop('user')
    return fl.redirect('/login')


@app.delete('/delete/<int:id>')
def delete(id):
    user = auth.get_user()
    if 'delete' not in user.user_permissions:
        return fl.render_template('404.html')
    try:
        with engine.connect() as con:
            q = con.execute(f'delete from \"User\" where id = {id}')
    except:
        return {'status': 'error'}
    return {'status': 200}


"""TASK 2 Async"""

""" Simulate sources returned json"""


@app.get('/source1')
def source1():
    id = list(range(1, 11))
    id.extend(list(range(31, 41)))
    data = [{
        'id': i,
        'name': f'Test {i}'
    } for i in id]
    return json.dumps(data)


@app.get('/source2')
def source2():
    id = list(range(11, 21))
    id.extend(list(range(41, 51)))
    data = [{
        'id': i,
        'name': f'Test {i}'
    } for i in id]
    return json.dumps(data)


@app.get('/source3')
def source3():
    id = list(range(21, 31))
    id.extend(list(range(51, 61)))
    data = [{
        'id': i,
        'name': f'Test {i}'
    } for i in id]
    """ Simulate an error """
    if random.randint(1, 5) == 2:
        return None
    return json.dumps(data)




async def data_procesed(data):
    """ procesed data return sorted list """
    sources = []
    for resp in data:
        if resp.status == 200:
            r = await resp.text()
            await asyncio.sleep(0)
            sources.extend(json.loads(r))
    sources.sort(key=lambda x: x['id'])
    return sources


@app.get('/getusers')
async def getusers():
    a = []
    for i in range(1, 4):
        task = asyncio.create_task(fetch(f'http://127.0.0.1:5000/source{i}'))
        a.append(task)
    responses = await asyncio.gather(*a)

    data = await data_procesed(responses)
    return fl.render_template_string('{% for d in data %} <p>{{ d.name }}<p> {% endfor %}', data=data)


if __name__ == '__main__':
    app.run()
