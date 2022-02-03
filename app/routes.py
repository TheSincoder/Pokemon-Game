from app import app
from .forms import PokeSearch, RegisterForm, LoginForm
from. models import User
from flask import render_template, request, flash, redirect, url_for
import requests
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        #We do the login Stuff
        username = request.form.get('username')
        password = request.form.get('password')
        u = User.query.filter_by(username = username).first()
        if u and u.check_hashed_password(password):
            # good email and password
            login_user(u)
            flash("Welcome to the PokeDevil's Colosseum", 'danger')
            return redirect(url_for('index')) #good login
        flash('Invalid Email and/or Password', 'primary')         
        return render_template('login.html.j2', form=form,) #bad login

    return render_template('login.html.j2',form=form)

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Create a new user
        try:
            new_user_data = {
                "username":form.username.data,
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            #create an empty User
            new_user_object = User()
            #build user with form data
            new_user_object.from_dict(new_user_data)
            #save user to the database
            new_user_object.save()
        except:
            flash('There was an enexpected Error creating your Account. Please Try Again', 'primary')
            #Error Return
            return render_template('register.html.j2', form=form)
        # If it worked
        flash('You have registered successfully', 'danger')
        return redirect(url_for('login'))
        
    #GET Return
    return render_template('register.html.j2', form = form)

@app.route('/party', methods=['GET', 'POST'])
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
            return render_template('party.html.j2', form=form, pokemon_party = user_pokemon)
        else:
            error_string = "Pokemon doesn't exist, maybe it's a Digimon or a Yugioh?"
            return render_template('party.html.j2', form=form, error = error_string)
    return render_template('party.html.j2', form=form)