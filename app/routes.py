from app import app
from .forms import PokeSearch

from flask import render_template, request
import requests

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/party', methods=['GET', 'POST'])
def party():
    form = PokeSearch()
    if request.method == 'POST' and form.validate_on_submit():
        
        search = request.form.get('search').lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{search}"
        response = requests.get(url)
        if response.ok:
            user_pokemon = []               
            poke_dict={
                "name":response.json()['forms'][0]['name'],
                "hp":response.json()['stats'][0]['base_stat'],
                "defense":response.json()['stats'][2]['base_stat'],
                "attack":response.json()['stats'][1]['base_stat'],
                "ability_1":response.json()['abilities'][0]['ability']['name'],
                "ability_2":response.json()['abilities'][1]['ability']['name'] if len(response.json()['abilities']) > 1 else '',
                "ability_3":response.json()['abilities'][2]['ability']['name'] if len(response.json()['abilities']) > 2 else '',                 
                "sprite": response.json()['sprites']['front_shiny']
                }
            user_pokemon.append(poke_dict)
            return render_template('party.html.j2', form=form, pokemon_party = user_pokemon)
        else:
            error_string = "Pokemon doesn't exist, maybe it's a Digimon or a Yugioh?"
            return render_template('party.html.j2', form=form, error = error_string)
    return render_template('party.html.j2', form=form)