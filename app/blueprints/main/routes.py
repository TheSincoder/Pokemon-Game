from .import bp as main #this makes it easier to know what's going on
from .forms import PokeSearch
from app.models import PokeParty, PokeUserJoin
from flask import render_template, request, flash, redirect, url_for
import requests
from flask_login import  login_required, current_user

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
            # new_user_pokemon = PokeParty()
            # new_user_pokemon.from_dict(poke_dict)
            # new_user_pokemon.save()
            # poke = PokeParty.query.filter(PokeParty.name==search).first()
            if not PokeParty.exists(poke_dict["name"]):
                new_poke = PokeParty()
                new_poke.from_dict(poke_dict)
                new_poke.save()
        

            user = current_user
            user.add_to_team(PokeParty.exists(poke_dict['name']))

            
            # if list(user.team) != []:
            #     flash(user.team)
            # else:
            #     user.team.append(poke)
            #     user.save()

            

            return render_template('party.html.j2', form=form, pokemon_party = user_pokemon)
        else:
            error_string = "Pokemon doesn't exist, maybe it's a Digimon or a Yugioh?"
            return render_template('party.html.j2', form=form, error = error_string)
    return render_template('party.html.j2', form=form)


@main.route('/view_team', methods=['GET'])
@login_required
def view_team():
    # access the joint table
    # take that pokemon id and grab the info on the PokeParty table
    # display each pokemon on the page

    team = current_user.team
    return render_template('view_team.html.j2', team = team)

@main.route('/remove/<int:id>')
@login_required
def remove(id):
    # make id = the specific pokemon i'm clicking on
    poke = PokeUserJoin.query.get((id, current_user.id))
    poke.remove()
    flash(f'You have removed pokemon from your Team', 'warning')
    return redirect(url_for('main.view_team'))


    # user = current_user
    #     user.remove_from_team(PokeParty.exists(poke_dict['name']))

# @main.route('/show_users')
# @login_required
# def show_users():
#     pass

# @main.route('/battle')
# @login_required
# def battle():
#     pass

