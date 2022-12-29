from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Float, Integer

engine = create_engine('sqlite:///db.sqlite')
Base = declarative_base()

class Gare(Base):
    __tablename__ = "Gare"

    id = Column(String, primary_key=True)
    code_uic = Column(String, nullable=True)
    nom_gare = Column(String, nullable=True)
    code_postal = Column(String, nullable=True)
    code_commune = Column(String, nullable=True)
    code_departement = Column(String, nullable=True)
    departement = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)

class LostItem(Base):
    __tablename__ = "Lost_Item"

    id = Column(String, primary_key=True)
    code_uic = Column(String, nullable=True)
    date = Column(String, nullable=False)
    type_objet = Column(String, nullable=False)
    gare = Column(String, nullable=True)
    date_restitution = Column(String, nullable=True)


class Temperature(Base):
    __tablename__ = "Temperature"
    
    departement_code = Column(String,  primary_key=True)
    date = Column(String,  primary_key=True)
    temperature = Column(Integer, nullable=True)

    
    
class Frequentation(Base):
    __tablename__ = "Frequentation"

    id = Column(String, primary_key=True)
    code_uic = Column(String, nullable=True)
    code_postal = Column(String, nullable=True)
    total_voyageurs_2016 = Column(String, nullable=True)
    total_voyageurs_2017 = Column(String, nullable=True)
    total_voyageurs_2018 = Column(String, nullable=True)
    total_voyageurs_2019 = Column(String, nullable=True)
    total_voyageurs_2020 = Column(String, nullable=True)
    total_voyageurs_2021 = Column(String, nullable=True)

Base.metadata.create_all(engine)

##### infos 

# La classe declarative_base est une classe fournie par SQLAlchemy qui sert de base pour la création de classes déclaratives. Les classes déclaratives sont des classes qui représentent des tables de base de données et qui permettent de définir leur structure, c'est-à-dire les colonnes et leurs types.

# Pour utiliser les classes déclaratives, vous devez d'abord créer une instance de declarative_base en appelant la fonction declarative_base. Vous pouvez ensuite définir une classe qui hérite de declarative_base et qui définit les colonnes de la table en utilisant des objets Column.