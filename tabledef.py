from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///Account.db', echo=True)
Base = declarative_base()

########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    admin = Column(Boolean)

#----------------------------------------------------------------------
    def __init__(self, username, password, admin):
        """"""
        self.username = username
        self.password = password
        self.admin = admin

# create tables
Base.metadata.create_all(engine)