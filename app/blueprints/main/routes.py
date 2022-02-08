from .import bp as main #this makes it easier to know what's going on
from .forms import PokeSearch, PokeAdd
from app.models import PokeParty
from flask import render_template, request, flash
import requests
from flask_login import  login_required

@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')



@main.route('/party', methods=['GET', 'POST'])
@login_required
def party():
    form = PokeSearch()
    if request.method == 'POST' and form.validate_on_submit():
        
        search = request.form.get('search')
        
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
            new_user_pokemon = PokeParty()
            new_user_pokemon.from_dict(poke_dict)
            new_user_pokemon.save()
            return render_template('party.html.j2', form=form, pokemon_party = user_pokemon)
        else:
            error_string = "Pokemon doesn't exist, maybe it's a Digimon or a Yugioh?"
            return render_template('party.html.j2', form=form, error = error_string)
    return render_template('party.html.j2', form=form)

# @main.route('/party', methods=['GET', 'POST'])
# @login_required
# def team():
    
#     form = PokeSearch()
#     form_1 = PokeAdd()
#     if request.method =='POST' and form.validate_on_submit():
#         confirm = request.form.get('confirm')
#         try:
#             new_poke_data = {
#                 "name":party().poke_dict['name'].data,
#                 "hp":form.hp.data,
#                 "defense":form.defense.data,
#                 "attack":form.attack.data,
#                 "ability_1":form.ability_1.data,
#                 "ability_2":form.ability_2.data,
#                 "ability_3":form.ability_3.data,                 
#                 "sprite": form.sprite.data,
#             }
#             new_user_pokemon = PokeParty()
#             new_user_pokemon.from_dict(new_poke_data)
#             new_user_pokemon.save()
#         except:
#             flash('There was an enexpected Error adding your pokemon. Please Try Again', 'warning')
#             #Error Return
#             return render_template('register.html.j2', form=form)
#         flash('You have successfully added the Pokemon to your Team', 'danger')
        
#     return render_template('party.html.j2', form=form, )

