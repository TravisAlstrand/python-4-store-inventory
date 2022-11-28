from models import (Base, session, Product, engine)
import datetime
import csv



if __name__ == '__main__':
  Base.metadata.create_all(engine)
  