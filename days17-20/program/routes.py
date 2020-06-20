import requests
from flask import render_template, request
from program import app

from datetime import datetime
import requests

@app.route('/')
@app.route('/index')
def index():
    timenow = str(datetime.today())
    return render_template('index.html', time=timenow)


@app.route('/100days')
def p100days():
    return render_template('100days.html')


@app.route('/chuck')
def chuck():
    joke = get_chuck_joke()
    return render_template('chuck.html', joke=joke)

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    pokemon = []
    if request.method == 'POST' and 'pokecolor' in request.form:
        color = request.form.get('pokecolor')
        pokemon = get_poke_colors(color)

    return render_template('pokemon.html', pokemon=pokemon)

def get_poke_colors(color: str):
    r = requests.get(f'https://pokeapi.co/api/v2/pokemon-color/{color.lower()}')
    pokedata = r.json()
    pokemon = [i['name'] for i in pokedata['pokemon_species']]
    return pokemon

def get_chuck_joke():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data['value']
