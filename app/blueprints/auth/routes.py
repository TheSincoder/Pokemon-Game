from .import bp as auth 

from .forms import RegisterForm, LoginForm, EditProfileForm
from app.models import User
from flask import render_template, request, flash, redirect, url_for
import requests
from flask_login import login_user, current_user, logout_user, login_required

@auth.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('main.index')) #good login
        flash('Invalid Email and/or Password', 'primary')         
        return render_template('login.html.j2', form=form,) #bad login

    return render_template('login.html.j2',form=form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('auth.login'))

@auth.route('/register', methods = ['GET', 'POST'])
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
        return redirect(url_for('auth.login'))
        
    #GET Return
    return render_template('register.html.j2', form = form)


# user_profile

@auth.route('/user_profile', methods=['GET','POST'])
def user_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
            "username":form.username.data,
            "first_name":form.first_name.data.title(),
            "last_name":form.last_name.data.title(),
            "email":form.email.data.lower(),
            "password":form.password.data
        }
        user_email = User.query.filter_by(email = form.email.data.lower()).first()
        user_username = User.query.filter_by(username = form.username.data).first()
        if user_email and user_email.email != current_user.email:
            flash('Email already in use','warning')
            return redirect(url_for('auth.user_profile'))
        elif user_username and user_username.username != current_user.username:
            flash('Username already in use','warning')
            return redirect(url_for('auth.user_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Updated', 'success')
        except: 
            flash('There was an unexpected Error. Please Try Again', 'danger')
            return redirect(url_for('auth.user_profile'))
        return redirect(url_for('main.index'))
    return render_template('user_profile.html.j2', form=form)