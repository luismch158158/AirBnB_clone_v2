#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

if models.storage_type == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""

    if models.storage_type == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(
            DateTime, default=datetime.utcnow(), nullable=False)
        updated_at = Column(
            DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
        else:
            if (not kwargs.get("id", 0)):
                self.id = str(uuid.uuid4())
            if (kwargs.get("created_at", 0)):
                kwargs["created_at"] = datetime.fromisoformat(
                    kwargs["created_at"])
            else:
                self.created_at = datetime.now()
            if (kwargs.get("updated_at", 0)):
                kwargs["updated_at"] = datetime.fromisoformat(
                    kwargs["updated_at"])
            else:
                self.updated_at = self.created_at
            # kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
            #                                          '%Y-%m-%dT%H:%M:%S.%f')
            # kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
            #                                          '%Y-%m-%dT%H:%M:%S.%f')
            if (kwargs.get("__class__", 0)):
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        items = self.__dict__.items()
        string = '_sa_instance_state'
        filter_dict = {k: v for k, v in items if (k != string)}
        return ("[{}] ({}) {}".format(self.__class__.__name__, self.id, filter_dict))

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        # print("Estoy en el to_dict")
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        # print(f'Soy el dictionary: {dictionary}')
        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
