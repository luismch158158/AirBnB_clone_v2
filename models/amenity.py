#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.review import Review
import models


class Amenity(BaseModel, Base):

    if models.storage_type == 'db':
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)

    else:
        name = ""
