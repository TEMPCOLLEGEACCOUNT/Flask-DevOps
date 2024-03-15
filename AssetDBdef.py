from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///AssetDB.db', echo=True)
Base = declarative_base()
class AssetDB(Base):
    """"""
    __tablename__ = "AssetDB"

    id = Column(Integer, primary_key=True)
    AssetName = Column(String)
    AssetDescription = Column(String)
    AssetNumber = Column(Integer)
    AssetNotes = Column(String)
    AssetSignedoff = Column(Boolean)

#----------------------------------------------------------------------
    def __init__(self, AssetName, AssetDescription, AssetNumber, AssetNotes, AssetSignedoff):
        """"""
        self.AssetName = AssetName
        self.AssetDescription = AssetDescription
        self.AssetNumber = AssetNumber
        self.AssetNotes = AssetNotes
        self.AssetSignedoff = AssetSignedoff
# create tables
Base.metadata.create_all(engine)