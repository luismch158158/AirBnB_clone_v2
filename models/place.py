#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
import models

if models.storage_type == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'), nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'), nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """

    if models.storage_type == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        # amenity_ids = Column()
        reviews = relationship("Review", backref="place", cascade="all")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 backref="place_amenities",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """"""
            new_list = []
            reviews_all = models.storage.all(Review)
            for value in reviews_all.values():
                if (value.place_id == self.id):
                    new_list.append(value)
            return new_list

        @property
        def amenities(self):
            """"""
            new_list = []
            amenities_all = models.storage.all(Amenity)
            for value in amenities_all.values():
                for i in range(len(self.amenity_ids)):
                    if (value.id == self.amenity_ids[i].id):
                        new_list.append(value)
            return new_list

        @amenities.setter
        def amenities(self, obj=None):
            """"""
            if (obj is not None and obj.__class__.__name__ == 'Amenity'):
                self.amenity_ids.append(obj)

        def append(self, obj=None):
            """"""
            self.amenities = obj
