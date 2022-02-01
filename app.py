from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/party', methods=['GET', 'POST'])
def party():
    if request.method == 'POST':
        name = request.form.get('pokemon')
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        if response.ok:
            user_pokemon = []               
            poke_dict={
                "name":response.json()['forms'][0]['name'],
                "hp":response.json()['stats'][0]['base_stat'],
                "defense":response.json()['stats'][2]['base_stat'],
                "attack":response.json()['stats'][1]['base_stat'],
                "ability_1":response.json()['abilities'][0]['ability']['name'],
                "ability_2":response.json()['abilities'][1]['ability']['name'],               
                "sprite": response.json()['sprites']['front_shiny']
                }
            user_pokemon.append(poke_dict)
            return render_template('party.html.j2', pokemon_party = user_pokemon)
        else:
            error_string = "Pokemon doesn't exist, maybe it's a Digimon or a Yugioh?"
            return render_template('party.html.j2', error = error_string)
    return render_template('party.html.j2')
    
    