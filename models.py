from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
  __tablename__ = 'products'

  product_id = Column(Integer, primary_key=True)
  product_name = Column(String)
  product_price = Column(Integer)
  product_quantity = Column(Integer)
  date_updated = Column(Date)

  def __repr__(self):
    return f'''Name: {self.product_name} - Price: {self.product_price} - Quantity: {self.product_quantity} - Date Updated: {self.date_updated}'''