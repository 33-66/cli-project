from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
# THE TABLES ARE  DISPLAYED HERE
class User(Base):
    # the user  table
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship('Task', back_populates='user')

class Task(Base):
    # tasks table 
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks')
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='tasks')

class Category(Base):
    #  categories of todos
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship('Task', back_populates='category')
