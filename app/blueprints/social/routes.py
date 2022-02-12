from .import bp as social
from flask import flash, redirect, url_for, render_template
from app.models import User
from flask_login import login_required, current_user

@social.route('/show_users')
@login_required
def show_users():
    users = User.query.all()
    return render_template('show_users.html.j2', users=users)

@social.route('/select_users')
@login_required
def select_user(id):
    user = User.query.get(id)
    return user

# @social.route('/select_user')
# @login_required
# def select_user(id):
#     user = User.query.get(id)
#     return user

@social.route('/battle/<int:id>', methods=['GET'])
@login_required
def battle(id):
    # select_user(id)
    user = User.query.get(id)
    if int(current_user.total_attack()) > int(user.total_attack()):
        current_user.wins += 1
        current_user.battles += 1
        current_user.save()
        flash(f'{current_user.username} has won!', 'danger')
    elif int(current_user.total_attack()) < int(user.total_attack()):
        current_user.losses += 1
        current_user.battles += 1
        current_user.save()
        flash(f'{user.username} has won!', 'light')
    else:
        current_user.battles += 1
        current_user.save()
        flash("It's a Tie!", 'warning')
        return redirect(url_for('social.show_users'))
    return redirect(url_for('social.show_users'))

