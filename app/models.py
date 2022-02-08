from app import db, login
from flask_login import UserMixin # This is just for the User Model!
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash


puj = db.Table(
    'puj',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokeparty_id', db.Integer, db.ForeignKey('pokeparty.id') )
)

# class PokeUserJoin(db.Model):
#     __tablename__ = 'pokeuserjoin'
#     # add pokemon and user combined
#     join_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     poke_id = db.Column(db.Integer, db.ForeignKey('pokeparty.id'))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    # party = db.relationship('PokeParty', secondary='puj')
    team = db.relationship(
        'PokeParty',
        secondary = puj,
        primaryjoin = (puj.c.user_id == id),
        back_populates='trainer',
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

    # def add_pokemon(self, user):
        

    #     return 


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
    name = db.Column(db.String(50))
    hp = db.Column(db.String(50))
    defense = db.Column(db.String(50))
    attack = db.Column(db.String(50))
    ability_1 = db.Column(db.String(50))
    ability_2 = db.Column(db.String(50))
    ability_3 = db.Column(db.String(50))
    sprite = db.Column(db.String(500))
    trainer = db.relationship(
        'User',
        secondary = puj,
        primaryjoin = (puj.c.pokeparty_id == id),
        back_populates='team',
        lazy='dynamic'
    )


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

    def delete(self):
        db.session.delete(self) # delete the post to the db session
        db.session.commit() # save everyuthing in the session to the database
        



    # def __repr__(self):
    #     return f'<Pokemon: {self.user_id} | {self.poke_id}>'

    # def save(self):
    #     db.session.add(self) # add the post to the db session
    #     db.session.commit() # save everyuthing in the session to the database

    # def from_dict(self, data):
    #     self.user_id = data['user_id']
    #     self.poke_id = data['poke_id']

    
    