from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    posting_time = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    image_url=Column(String)

        
class Animal(Base):
    __tablename__ = 'animals'
    animal_id= Column(Integer, primary_key=True, nullable=False)
    species = Column(String)
    gender = Column(String)
    description = Column(String)
    image_url = Column(String)
    available = Column(Boolean,server_default='True')

                                                                                                                                                                                                                                                                                                                                                                                                                                              
class Adoption(Base):
    __tablename__ = "adoption"
    adoption_id = Column(Integer, primary_key=True, nullable=False )
    animal_id = Column(Integer)
    adopter_name = Column(String)
    adopter_email = Column(String )
    adopter_phone = Column(String)
    #animal = relationship("Animals", back_populates="adoption")


                                
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

