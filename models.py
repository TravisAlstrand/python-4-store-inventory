from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product():
  __tablename__ = 'products'

  id = Column(Integer, primary_key=True)
  name = Column('Name', String)
  price = Column('Price', Integer)
  quantity = Column('Quantity', Integer)
  date_updated = Column('Date Updated', Date)

  def __repr__(self):
    return f'''Name: {self.name} - Price: {self.price} -
            Quantity: {self.quantity} - Date Updated: {self.date_updated}'''