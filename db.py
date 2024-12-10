from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, Text, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/kr2'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class CarModel(Base):
    __tablename__ = "car_model"
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))

class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key = True, autoincrement = True)
    model_id = Column(Integer, ForeignKey("car_model.id"))
    number = Column(String(50))
    color = Column(String(50))
    release_year = Column(Date)
    insurence_cost = Column(Integer)
    fk_model_id = relationship("CarModel")

class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key = True, autoincrement = True)
    lastname = Column(String(50))
    firstname = Column(String(50))
    patronymic = Column(String(50))
    series_passport = Column(Integer)
    number_passport = Column(Integer)

class Rental(Base):
    __tablename__ = "rental"
    id = Column(Integer, primary_key = True, autoincrement = True)
    day_cost = Column(Integer)
    start_date = Column(Date)
    days_quantity = Column(Integer)
    car_id = Column(Integer, ForeignKey("car.id"))
    fk_car_id = relationship("Car")
    client_id = Column(Integer, ForeignKey("client.id"))
    fk_client_id = relationship("Client")

def get_session():
    return session