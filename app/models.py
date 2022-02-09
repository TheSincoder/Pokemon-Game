from app import db, login
from flask_login import UserMixin # This is just for the User Model!
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash




class PokeUserJoin(db.Model):
    pokeparty_id = db.Column(db.Integer, db.ForeignKey('pokeparty.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    team = db.relationship(
        'PokeParty',
        secondary = 'poke_user_join',
        backref= 'users',        
        lazy='dynamic'
    )


    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'
    #salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def collect_poke(self, poke):
        self.team.append(poke)
        db.session.commit()
        

    

    def add_to_team(self, Obj):
        if len(list(self.team)) <= 5:
            self.team.append(Obj)
            self.save()

    def remove_from_team(self, Obj):
        if len(list(self.team)) > 0:
            self.team.remove(Obj)
            self.save()


    def from_dict(self, data):
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    # saves the user to the database
    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit() # save everyuthing in the session to the database

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# create a joint table to store pokemon
# adding pokemon is a many to many relationship

class PokeParty(db.Model):
    __tablename__ = 'pokeparty'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    hp = db.Column(db.String(50))
    defense = db.Column(db.String(50))
    attack = db.Column(db.String(50))
    ability_1 = db.Column(db.String(50))
    ability_2 = db.Column(db.String(50))
    ability_3 = db.Column(db.String(50))
    sprite = db.Column(db.String(500))
    


    def __repr__(self):
        return f'<Pokemon: {self.id} | {self.name}>'

    def from_dict(self, data):
        self.name = data['name']
        self.hp = data['hp']
        self.defense = data['defense']
        self.attack = data['attack']
        self.ability_1 = data['ability_1']
        self.ability_2 = data['ability_2']
        self.ability_3 = data['ability_3']
        self.sprite = data['sprite']



    def save(self):
        db.session.add(self) # add the post to the db session
        db.session.commit() # save everyuthing in the session to the database

    def exists(name):
         return PokeParty.query.filter_by(name=name).first()

    def delete(self):
        db.session.delete(self) # delete the post to the db session
        db.session.commit() # save everyuthing in the session to the database
        



# to check if the user has 5 pokemon
# if len(list(current_user.team)) <= 5:

