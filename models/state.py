#!/usr/bin/python3
import models
from os import getenv
from models.base_model import BaseModel ,Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

""" State Module for HBNB project """


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(string(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")
    
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """getter for cities"""
            all_cities = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    all_cities.append(city)
            return all_cities
