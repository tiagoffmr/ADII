#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 4 - servidor.py
Grupo: 13
Números de aluno: 51595 - Diogo Frazão,
                  51628 - Tiago Robalo,
                  51636 - Vasco Bento
"""
#Zona para fazer imports

import spotify
import sqlite3
from flask import Flask, request, make_response, g
import json
from os.path import isfile
import ssl
import requests
import os

#Informação sobre o authorization server

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

#Programa principal

dbName = "bd.db"

app = Flask(__name__)

@app.before_first_request
def before_first_request():
    init_db()

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def init_db():
    with app.app_context():
        db_is_created = isfile(dbName)
        db = get_db()
        if not db_is_created:
            with app.open_resource('dbInicial.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(dbName)
    return db

tokens = []

def authenticate(data):
    if data['access_token'] in tokens:
        return True
    else:
        return False

@app.route('/login', methods = ["GET"])
def login():
    data = json.loads(request.data)
    headers = {'Authorization': 'token ' + data['access_token']}
    resp = requests.get('https://api.github.com/user', headers=headers)
    response = json.loads(resp.content)
    if 'login' in response:
        r = make_response(json.dumps("Utilizador logado com sucesso."))
        r.status_code = 200
        tokens.append(data['access_token'])
    else:
        r = make_response(json.dumps("Falha na autenticacao do utilizador."))
        r.status_code = 401
    return r

#--------------------------------------------- UTILIZADORES ---------------------------------------------

@app.route('/utilizadores', methods = ["PUT", "POST", "GET", "DELETE"])
@app.route('/utilizadores/<int:id>', methods = ["GET", "DELETE"])

def utilizadores(id = None):
        data = json.loads(request.data)

        if authenticate(data['token']):
            conn, cursor = (g.db, g.db.cursor())

            if request.method == "GET":
                if id == None: #SHOW ALL USERS
                    cursor.execute("SELECT * FROM utilizadores")
                else: #SHOW USER <id>
                    cursor.execute("SELECT * FROM utilizadores WHERE id = {0}".format(id))
                resultado = cursor.fetchall()
                if len(resultado) > 0:
                    r = make_response(json.dumps(resultado))
                    r.status_code = 200
                else:
                    r = make_response(json.dumps("Utilizador(es) nao encontrado(s)."))
                    r.status_code = 404


            if request.method == "POST": #ADD USER <nome> <utilizador> <password>
                nome = data['nome']
                username = data['username']
                password = data['password']
                cursor.execute("INSERT INTO utilizadores (nome, username, password) VALUES (?, ?, ?)", (nome, username, password))
                conn.commit()
                r = make_response(json.dumps("Utilizador Inserido."))
                r.status_code = 201

            if request.method == "DELETE":
                if id == None: #REMOVE ALL USERS
                    query = cursor.execute("DELETE FROM utilizadores WHERE id NOT IN (SELECT la.id_user FROM listas_albuns la)")
                    conn.commit()
                    r = make_response(json.dumps("Utilizador(es) Removido(s) que nao tem rates associados."))
                    r.status_code = 200
                else: #REMOVE USER <id>
                    cursor.execute("SELECT * FROM utilizadores WHERE id = {0}".format(id))
                    nUser = cursor.fetchall()
                    if len(nUser) == 1:
                        cursor.execute("SELECT * FROM listas_albuns WHERE id_user = {0}".format(id))
                        user = cursor.fetchall()
                        if len(user) == 0:
                            query = cursor.execute("DELETE FROM utilizadores WHERE id = {0}".format(id))
                            conn.commit()
                            r = make_response(json.dumps("Utilizador Removido."))
                            r.status_code = 200
                        else:
                            r = make_response(json.dumps("Utilizador tem rate(s) associado(s). Nao e possivel remover."))
                            r.status_code = 403
                    else:
                        r = make_response(json.dumps("Utilizador nao encontrado."))
                        r.status_code = 404

            if request.method == "PUT": #UPDATE USER <id> <password>
                data = json.loads(request.data)
                id_user = data['id_user']
                password = data['password']
                query = cursor.execute("SELECT * FROM utilizadores WHERE id = '{0}'".format(id_user))
                user = cursor.fetchall()
                if len(user) == 1:
                    query = cursor.execute("UPDATE utilizadores SET password = '{0}' WHERE id = {1}".format(password, id_user))
                    conn.commit()
                    r = make_response(json.dumps("Dados Atualizados."))
                    r.status_code = 200
                else:
                    r = make_response(json.dumps("Utilizador nao exite."))
                    r.status_code = 403

            return r

        else:
            r = make_response(json.dumps("Utilizador nao se encontra autenticado."))
            r.status_code = 403
            return r

#--------------------------------------------- BANDAS ---------------------------------------------

@app.route('/bandas', methods = ["PUT", "POST", "GET", "DELETE"])
@app.route('/bandas/<int:id>', methods = ["GET", "DELETE"])

def bandas(id = None):
    dic = json.loads(request.data)
        
    if authenticate(dic['token']):
        conn, cursor = (g.db, g.db.cursor())

        if request.method == "GET":
            if id == None: #SHOW ALL BANDAS
                query = cursor.execute("SELECT * FROM bandas")
            else: #SHOW BANDA <id>
                query = cursor.execute("SELECT * FROM bandas WHERE id = {0}".format(id))
            resultado = cursor.fetchall()
            if len(resultado) > 0:
                for i in range(len(resultado)):
                    resultado.append(spotify.show_banda(resultado[i][1])) #Spotify - info sobre banda
                r = make_response(json.dumps(resultado))
                r.status_code = 200
            else:
                r = make_response(json.dumps("Banda nao encontrada."))
                r.status_code = 404

        if request.method == "POST": #ADD BANDA <nome> <ano> <genero>
            data = json.loads(request.data)
            nome = data['nome']
            ano = data['ano']
            genero = data['genero']
            cursor.execute("INSERT INTO bandas (nome, ano, genero) VALUES (?, ?, ?)", (nome, ano, genero))
            conn.commit()
            r = make_response(json.dumps("Banda Inserida."))
            r.status_code = 201

        if request.method == "DELETE":
            if id == None: #REMOVE ALL BANDS
                query = cursor.execute("DELETE FROM bandas WHERE id NOT IN (SELECT a.id FROM albuns a)")
                conn.commit()
                r = make_response(json.dumps("Bandas removidas que nao tem albuns associados. Para remover todas as bandas, tera de remover os albuns desta."))
                r.status_code = 200
            else: #REMOVE BAND <id>
                cursor.execute("SELECT * FROM bandas WHERE id = {0}".format(id))
                nBanda = cursor.fetchall()
                if len(nBanda) == 1:
                    cursor.execute("SELECT * FROM albuns WHERE id = {0}".format(id))
                    album = cursor.fetchall()
                    if len(album) == 0:
                        query = cursor.execute("DELETE FROM bandas WHERE id = {0}".format(id))
                        conn.commit()
                        if query:
                            r = make_response(json.dumps("Banda removida."))
                            r.status_code = 200
                    else:
                        r = make_response(json.dumps("Banda tem album(s) associado(s). Nao e possivel remover."))
                        r.status_code = 403
                else:
                    r = make_response(json.dumps("Banda nao encontrada."))
                    r.status_code = 404

        return r

    else:
        r = make_response(json.dumps("Utilizador nao se encontra autenticado."))
        r.status_code = 403
        return r

#--------------------------------------------- ALBUNS ---------------------------------------------

@app.route('/albuns', methods = ["PUT", "POST", "GET", "DELETE"])
@app.route('/albuns/<int:id>', methods = ["DELETE", "GET"])
@app.route('/albuns/<rate>', methods = ["PUT", "POST"])

def albuns(id = None, rate = None):
    dic = json.loads(request.data)
        
    if authenticate(dic['token']):
        conn, cursor = (g.db, g.db.cursor())
        if request.method == "GET":
            if id == None:
                if request.data:
                    dados = json.loads(request.data)
                    if 'id_banda' in dados.keys(): #SHOW ALL ALBUNS_B <id_banda>
                        query = cursor.execute("SELECT * FROM albuns WHERE id_banda = {0}".format(dados['id_banda']))
                    elif 'id_user' in dados.keys(): #SHOW ALL ALBUNS_U <id_user>
                        query = cursor.execute("SELECT * FROM albuns WHERE id IN (SELECT id_album FROM listas_albuns WHERE id_user = {0})".format(dados['id_user']))
                    elif 'rate' in dados.keys(): #SHOW ALL ALBUNS <rate>
                        query = cursor.execute("SELECT id FROM rates WHERE sigla='{0}'".format(dados['rate']))
                        id_rate = cursor.fetchone()[0]
                        query = cursor.execute("SELECT * FROM albuns WHERE id IN (SELECT id_album FROM listas_albuns WHERE id_rate = {0})".format(id_rate))
                else: #SHOW ALL ALBUMS
                    query = cursor.execute("SELECT * FROM albuns")
            else: #SHOW ALBUM <id>
                query = cursor.execute("SELECT * FROM albuns WHERE id = {0}".format(id))
            resposta = cursor.fetchall()
            if len(resposta) > 0:
                for i in range(len(resposta)):
                    resposta.append(spotify.show_album(resposta[i][2])) #Spotify - info sobre album
                r = make_response(json.dumps(resposta))
                r.status_code = 200
            else:
                r = make_response(json.dumps("Album nao existe."))
                r.status_code = 404

        if request.method == "POST": #ADD ALBUM <id_banda> <nome> <ano_album>
            if rate == None:
                data = json.loads(request.data)
                id_banda = data['id_banda']
                nome = data['nome']
                ano_album = data['ano_album']
                cursor.execute("SELECT * FROM bandas WHERE id = {0}".format(id_banda))
                resposta = cursor.fetchall()
                if len(resposta) == 1:
                    cursor.execute("INSERT INTO albuns (id_banda, nome, ano_album) VALUES (?, ?, ?)", (id_banda, nome, ano_album))
                    conn.commit()
                    r = make_response(json.dumps("Album Inserido."))
                    r.status_code = 201
                else:
                    r = make_response(json.dumps("Não existe(m) banda(s)."))
                    r.status_code = 404

            else: #ADD <id_user> <id_album> <rate>
                data = json.loads(request.data)
                id_user = data['id_user']
                id_album = data['id_album']
                cursor.execute("SELECT id FROM rates WHERE sigla='{0}'".format(rate))
                id_rate = cursor.fetchone()[0]
                cursor.execute("SELECT * FROM utilizadores WHERE id = {0}".format(id_user))
                utilizador = cursor.fetchall()
                cursor.execute("SELECT * FROM albuns WHERE id = {0}".format(id_album))
                album = cursor.fetchall()
                if len(utilizador) > 0 and len(album) > 0:
                    try:
                        cursor.execute("INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES (?, ?, ?)", (id_user, id_album, id_rate))
                        conn.commit()
                        r = make_response(json.dumps("Album Classificado."))
                        r.status_code = 201
                    except:
                        r = make_response(json.dumps("Album ja classificado. Use o Comando UPDATE."))
                        r.status_code = 406
                else:
                    r = make_response(json.dumps("Album/Utilizador nao existe."))
                    r.status_code = 403

        if request.method == "DELETE":
            if id == None:
                if request.data:
                    dados = json.loads(request.data)
                    if 'id_banda' in dados.keys(): #REMOVE ALL ALBUNS_B <id_banda>
                        query = cursor.execute("DELETE FROM albuns WHERE id_banda = {0} AND id NOT IN (SELECT la.id_album FROM listas_albuns la)".format(dados['id_banda']))
                        conn.commit()
                        r = make_response(json.dumps("Albuns removidos que nao tem rates associados."))
                        r.status_code = 200
                    elif 'id_user' in dados.keys(): #REMOVE ALL ALBUNS_U <id_user>
                        query = cursor.execute("DELETE FROM albuns WHERE id IN (SELECT id_album FROM listas_albuns WHERE id_user = {0})".format(dados['id_user']))
                        cursor.execute("DELETE FROM listas_albuns WHERE id_user = {0}".format(dados['id_user']))
                        conn.commit()
                        r = make_response(json.dumps("Albuns com rates do utilizador removidos."))
                        r.status_code = 200
                    elif 'rate' in dados.keys(): #REMOVE ALL ALBUNS <rate>
                        query = cursor.execute("SELECT id FROM rates WHERE sigla='{0}'".format(dados['rate']))
                        id_rate = cursor.fetchone()[0]
                        query = cursor.execute("DELETE FROM albuns WHERE id IN (SELECT id_album FROM listas_albuns WHERE id_rate = {0})".format(id_rate))
                        cursor.execute("DELETE FROM listas_albuns WHERE id_rate = {0}".format(id_rate))
                        conn.commit()
                        r = make_response(json.dumps("Albuns com rates removidos."))
                        r.status_code = 200
                else: #REMOVE ALL ALBUNS
                    query = cursor.execute("DELETE FROM albuns WHERE id NOT IN (SELECT la.id_album FROM listas_albuns la)")
                    conn.commit()
                    r = make_response(json.dumps("Albuns removidos que nao tem rates associados."))
                    r.status_code = 200
            else: #REMOVE ALBUM <id>
                cursor.execute("SELECT * FROM albuns WHERE id = {0}".format(id))
                nAlbum = cursor.fetchall()
                if len(nAlbum) == 1:
                    cursor.execute("SELECT * FROM listas_albuns WHERE id_album = {0}".format(id))
                    rates = cursor.fetchall()
                    if len(rates) == 0:
                        cursor.execute("DELETE FROM albuns WHERE id = {0}".format(id))
                        conn.commit()
                        r = make_response(json.dumps("Album removido."))
                        r.status_code = 200
                    else:
                        r = make_response(json.dumps("Album tem rate(s) associado(s). Nao e possivel remover."))
                        r.status_code = 403
                else:
                    r = make_response(json.dumps("Album nao encontrado."))
                    r.status_code = 404

        if request.method == "PUT": #UPDATE ALBUM <id_u> <id_album> <rate>
            data = json.loads(request.data)
            id_user = data['id_user']
            id_album = data['id_album']
            rate = data['rate']
            cursor.execute("SELECT * FROM listas_albuns WHERE id_user = {0} and id_album = {1}".format(id_user,id_album))
            rating = cursor.fetchall()
            if len(rating) == 1:
                query = cursor.execute("SELECT id FROM rates WHERE sigla='{0}'".format(rate))
                id_rate = cursor.fetchone()[0]
                query = cursor.execute("UPDATE listas_albuns SET id_rate = {0} WHERE id_user = {1} AND id_album = {2}".format(id_rate, id_user, id_album))
                conn.commit()
                r = make_response(json.dumps("Atualizado com sucesso."))
                r.status_code = 200
            else:
                r = make_response(json.dumps("Rate nao existe."))
                r.status_code = 403

        return r

    else:
        r = make_response(json.dumps("Utilizador nao se encontra autenticado."))
        r.status_code = 401
        return r

if __name__ == '__main__':

#========================== SSL CONTEXT =======================================
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    context.load_cert_chain('../certs/server.crt', '../certs/server.key')
    context.load_verify_locations('../certs/root.pem')
#==============================================================================

    app.run(ssl_context=context, threaded=True, debug=True)
