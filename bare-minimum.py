#!/usr/bin/env python3

import sqlalchemy as s
from sqlalchemy import create_engine as ce
from sqlalchemy.ext.declarative import declarative_base as db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker as sm
from sqlalchemy.orm import relationship

engine = ce('sqlite:///:memory:', echo=True)
Base = db()
Session = sm(bind=engine)

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  addresses = relationship('Address', back_populates="user")

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return 'I\'m a user.'


class Address(Base):
  __tablename__ = 'addresses'
  
  id = Column(Integer, primary_key=True)
  email = Column(String, nullable=False)

  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship('User', back_populates='addresses')

  def __init__(self, email):
    self.email = email

#  User.addresses = relationship('Address', back_populates="user")

Base.metadata.create_all(engine)

sample_user = User('Julien')
sample_address_1 = Address('julienchurch@gmail.com')

session = Session()
session.add(sample_user)
session.commit()

julien = session.query(User).filter_by(name='Julien').one()
