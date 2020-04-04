#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 4 - cliente.py
Grupo: 13
Números de aluno: 51595 - Diogo Frazão,
                  51628 - Tiago Robalo,
                  51636 - Vasco Bento
"""
#Zona para fazer imports

import requests
import json
from requests_oauthlib import OAuth2Session
import os

session = requests.session()
session.cert = ('../certs/client.crt', '../certs/client.key')
session.verify = '../certs/root.pem'

# Programa principal

print('\nBem-vindo\n')


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'                                             #Para nao suportar ligacao HTTPS
client_id = '786767bd0f46d849e02a'                                                          #Credenciais obtidas da API github no registo da aplicação
client_secret = '0c5f47fb7b0729efff200313c363b81f50c219f2'
authorization_base_url = 'https://github.com/login/oauth/authorize'                         #Servidores da github para obtencao do authorization_code e do token
token_url = 'https://github.com/login/oauth/access_token'

github = OAuth2Session(client_id)
authorization_url, state = github.authorization_url(authorization_base_url)                 #Pedido do authorization_code ao servidor de autorização (e dono do recuro a aceder)
print('Aceder ao link (via browser) para obter a autorizacao,', authorization_url)
redirect_response = input('Insira o URL devolvido no browser e cole aqui: ')                #Obter o authorization_code do servidor vindo no URL de redireccionamento
token = github.fetch_token(token_url, client_secret=client_secret,
                           authorization_response=redirect_response)

r = requests.get('https://localhost:5000/login', json = token, verify = False)
cnt = json.loads(r.content.decode())
print()
print(r.status_code)
print(cnt)
print('---------------------\n')

if r.status_code == 200:

    genero = ['pop', 'rock', 'indy', 'metal', 'trance']
    ratings = ['M', 'MM', 'S', 'B', 'MB']

    cmd = ""
    while cmd != "EXIT":
        cmd = input("Comando > ")
        cmdS = cmd.split(" ")

        error = False

        if cmdS[0] == "ADD":
            if len(cmdS) == 5:
                if cmdS[1] == "USER":
                    nome = cmdS[2].replace("_", " ")
                    data = {'nome': nome, 'username': cmdS[3], 'password': cmdS[4], 'token': token}
                    try:
                        r = session.post('https://localhost:5000/utilizadores', json=data, verify=False)
                    except:
                        print("Erro na ligação com o servidor.")
                        error = True
                elif cmdS[1] == "BANDA":
                    nome = cmdS[2].replace("_", " ")
                    try:
                        if cmdS[4] in genero:
                            data = {'nome': nome, 'ano': int(cmdS[3]), 'genero': cmdS[4], 'token': token}
                            try:
                                r = session.post('https://localhost:5000/utilizadores', json=data, verify=False)
                            except:
                                print("Erro na ligação com o servidor.")
                                error = True
                        else:
                            print("Genero Desconhecido. Generos Possíveis: pop, rock, indy, metal, trance")
                            error = True
                    except:
                        print("Os anos tem de ser números inteiros.")
                        error = True
                elif cmdS[1] == "ALBUM":
                    try:
                        nome = cmdS[3].replace("_", " ")
                        data = {'id_banda': int(cmdS[2]), 'nome': nome, 'ano_album': int(cmdS[4]), 'token': token}
                        try:
                            r = session.post('https://localhost:5000/utilizadores', json=data, verify=False)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    except:
                        print("Os id's e anos tem de ser números inteiros.")
                        error = True
                else:
                    print("Comando Desconhecido.")
                    error = True
            elif len(cmdS) == 4:
                if cmdS[3] in ratings:
                    try:
                        data = {'id_user': int(cmdS[1]), 'id_album': int(cmdS[2]), 'token': token}
                        try:
                            r = session.post('https://localhost:5000/utilizadores', json=data, verify=False)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    except:
                        print("Os id's tem de ser números inteiros.")
                        error = True
                else:
                    print("Rating Desconhecido. Ratings Possíveis: M, MM, S, B ou MB.")
                    error = True
            else:
                print("Comando Desconhecido.")
                error = True

        elif cmdS[0] == "REMOVE":
            if len(cmdS) == 3:
                data = {'token': token}
                if cmdS[1] == "USER":
                    try:
                        r = session.delete('https://localhost:5000/utilizadores/%s' %(str(cmdS[2])), verify=False, json=data)
                    except:
                        print("Erro na ligação com o servidor.")
                        error = True
                elif cmdS[1] == "BANDA":
                    try:
                        r = session.delete('https://localhost:5000/bandas/%s' %(str(cmdS[2])), verify=False, json=data)
                    except:
                        print("Erro na ligação com o servidor.")
                        error = True
                elif cmdS[1] == "ALBUM":
                    try:
                        r = session.delete('https://localhost:5000/albuns/%s' %(str(cmdS[2])), verify=False, json=data)
                    except:
                        print("Erro na ligação com o servidor.")
                        error = True
                elif cmdS[1] == "ALL":
                    if cmdS[2] == "USERS":
                        try:
                            r = session.delete('https://localhost:5000/utilizadores', verify=False, json=data)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    elif cmdS[2] == "BANDAS":
                        try:
                            r = session.delete('https://localhost:5000/bandas', verify=False, json=data)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    elif cmdS[2] == "ALBUNS":
                        try:
                            r = session.delete('https://localhost:5000/albuns', verify=False, json=data)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    else:
                        print("Comando Desconhecido.")
                        error = True
                else:
                    print("Comando Desconhecido.")
                    error = True
            elif cmdS[1] == "ALL" and len(cmdS) == 4:
                if cmdS[2] == "ALBUNS_B":
                    try:
                        data = {'id_banda': int(cmdS[3]), 'token': token}
                        try:
                            r = session.delete('https://localhost:5000/albuns', verify=False, json=data)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    except:
                        print("Os id's tem de ser números inteiros.")
                        error = True
                elif cmdS[2] == "ALBUNS_U":
                    try:
                        data = {'id_user': int(cmdS[3]), 'token': token}
                        try:
                            r = session.delete('https://localhost:5000/albuns', verify=False, json=data)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    except:
                        print("Os id's tem de ser números inteiros.")
                        error = True
                elif cmdS[2] == "ALBUNS":
                    if cmdS[3] in ratings:
                        data = {'rate': cmdS[3], 'token': token}
                        try:
                            r = session.delete('https://localhost:5000/albuns', verify=False, json=data)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    else:
                        print("Rating Desconhecido. Ratings Possíveis: M, MM, S, B ou MB.")
                        error = True
                else:
                    print("Comando Desconhecido.")
                    error = True
            else:
                print("Comando Desconhecido.")
                error = True

        elif cmdS[0] == "SHOW" and len(cmdS) > 1:
            if len(cmdS) == 3:
                data = {'token': token}
                if cmdS[1] == "USER":
                    try:
                        r = session.get('https://localhost:5000/utilizadores/%s' %(str(cmdS[2])), verify=False, json=data)
                    except:
                        print("Erro na ligação com o servidor.")
                        error = True
                elif cmdS[1] == "BANDA":
                    try:
                        r = session.get('https://localhost:5000/bandas/%s' %(str(cmdS[2])), verify=False, json=data)
                    except:
                        print("Erro na ligação com o servidor.")
                        error = True
                elif cmdS[1] == "ALBUM":
                    try:
                        r = session.get('https://localhost:5000/albuns/%s' %(str(cmdS[2])), verify=False, json=data)
                    except:
                        print("Erro na ligação com o servidor.")
                        error = True
                elif cmdS[1] == "ALL":
                    if cmdS[2] == "USERS":
                        try:
                            r = session.get('https://localhost:5000/utilizadores', verify=False, json=data)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    elif cmdS[2] == "BANDAS":
                        try:
                            r = session.get('https://localhost:5000/bandas', verify=False, json=data)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    elif cmdS[2] == "ALBUNS":
                        try:
                            r = session.get('https://localhost:5000/albuns', verify=False, json=data)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    else:
                        print("Comando Desconhecido.")
                        error = True
                else:
                    print("Comando Desconhecido.")
                    error = True
            elif cmdS[1] == "ALL" and len(cmdS) == 4:
                if cmdS[2] == "ALBUNS_B":
                    try:
                        data = {'id_banda': int(cmdS[3]), 'token': token}
                        try:
                            r = session.get('https://localhost:5000/albuns', json=data, verify=False)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    except:
                        print("Os id's tem de ser números inteiros.")
                        error = True
                elif cmdS[2] == "ALBUNS_U":
                    try:
                        data = {'id_user': int(cmdS[3]), 'token': token}
                        try:
                            r = session.get('https://localhost:5000/albuns', json=data, verify=False)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    except:
                        print("Os id's tem de ser números inteiros.")
                        error = True
                elif cmdS[2] == "ALBUNS":
                    if cmdS[3] in ratings:
                        data = {'rate': cmdS[3], 'token': token}
                        try:
                            r = session.get('https://localhost:5000/albuns', json=data, verify=False)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    else:
                        print("Rating Desconhecido. Ratings Possíveis: M, MM, S, B ou MB.")
                        error = True
                else:
                    print("Comando Desconhecido.")
                    error = True
            else:
                print("Comando Desconhecido.")
                error = True

        elif cmdS[0] == "UPDATE":
            if cmdS[1] == "ALBUM" and len(cmdS) == 5:
                if cmdS[4] in ratings:
                    try:
                        data = {'id_user': int(cmdS[2]), 'id_album': int(cmdS[3]), 'rate': cmdS[4], 'token': token}
                        try:
                            r = session.put('https://localhost:5000/albuns', json=data, verify=False)
                        except:
                            print("Erro na ligação com o servidor.")
                            error = True
                    except:
                        print("Os id's tem de ser números inteiros.")
                        error = True
                else:
                    print("Rating Desconhecido. Ratings Possíveis: M, MM, S, B ou MB.")
                    error = True
            elif cmdS[1] == "USER" and len(cmdS) == 4:
                try:
                    data = {'id_user': int(cmdS[2]), 'password': cmdS[3], 'token': token}
                    try:
                        r = session.put('https://localhost:5000/utilizadores', json=data, verify=False)
                    except:
                        print("Erro na ligação com o servidor.")
                        error = True
                except:
                    print("Os id's tem de ser números inteiros.")
                    error = True
            else:
                print("Comando Desconhecido.")
                error = True

        else:
            if cmd != "EXIT":
                print("Comando Desconhecido.")
                error = True

        if not error:
            cnt = json.loads(r.content.decode())
            print(r.status_code)
            if isinstance(cnt, list):
                for i in cnt:
                    for j in i:
                        print(j,end='\t\t')
                    print(end='\n')
            else:
                print(cnt)
                if r.status_code == 401:
                    cmd = "EXIT"
        print('---------------------\n')
