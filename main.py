from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from tabulate import tabulate

engine = create_engine('sqlite:///sql/bdd.sqlite', echo=True)

Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"User(name='{self.name}', age={self.age})"

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    street = Column(String)
    city = Column(String)
    postal_code = Column(String)
    user = relationship('User', backref='posts')

    def __repr__(self):
        return f"PostTitle='{self.title}', content='{self.content}'"

Base.metadata.create_all(engine)

user1 = User(name="Quentin", age=23)
user2 = User(name="Matthias", age=24)

session.add(user1)
session.add(user2)
session.commit()

adress1 = Address(user_id=user1.id, street='Dans la lironde', city='Montpellier', postal_code='34000')
adress2 = Address(user_id=user2.id, street='Quelquepart dans les rues mentonnaises', city='Menton', postal_code='06500')

session.add(adress1)
session.add(adress2)
session.commit()

query = session.query(User, Address).join(Address, User.id == Address.user_id)

results = query.all()

data = [(user.name, user.age, address.street, address.city, address.postal_code) for user, address in results]

# En-têtes pour les colonnes de notre tableau
headers = ['User Name', 'Age', 'Street', 'City', 'Postal Code']

# Création et affichage du tableau
table = tabulate(data, headers=headers, tablefmt='grid')
print(table)