#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 4 - spotify.py
Grupo: 13
Números de aluno: 51595 - Diogo Frazão,
                  51628 - Tiago Robalo,
                  51636 - Vasco Bento
"""
#Zona para fazer imports

import requests
import json
import os
import ast

get_at = 'curl -X "POST" -H "Authorization: Basic OWRmNzQzY2E5ZDNkNDc1NmEyNTQwMWI4Y2EzYjMwMjc6NDNmNjQ3ZTA5ZmZjNDg3NzgwZjBiZDVhMGNmOThkN2I=" -d grant_type=client_credentials https://accounts.spotify.com/api/token'
access_token = ast.literal_eval(os.popen(get_at).read())

#Programa principal

def show_banda(banda):
    url = "https://api.spotify.com/v1/search?q=" + str(banda) + "&type=artist&market=us&limit=1"
    try:
        r = json.loads(requests.get(url, access_token).content.decode('utf-8'))
        name = r['artists']['items'][0]['name']
        genre = r['artists']['items'][0]['genres']
        followers = r['artists']['items'][0]['followers']['total']
        popularity = r['artists']['items'][0]['popularity']
        return [name, genre, followers, popularity]
    except:
        return ["Token Inválido"]


def show_album(album):
    url = "https://api.spotify.com/v1/search?q=" + str(album) + "&type=album&market=us&limit=1"
    try:
        r = json.loads(requests.get(url, access_token).content.decode('utf-8'))
        name = r['albums']['items'][0]['name']
        year = r['albums']['items'][0]['release_date'].split('-')[0]
        artist = r['albums']['items'][0]['artists'][0]['name']
        tracks = r['albums']['items'][0]['total_tracks']
        return [name, year, artist, tracks]
    except:
        return ["Token Inválido"]
