from models import (Base, session, Product, engine)
import datetime
import csv


def clean_price(price_str):
  try:
    no_currency = price_str.replace('$', '')
    price_float = float(no_currency)
  except ValueError:
    input('''
          \n*** PRICE ERROR ***
          \rThe price should be a number without a currency symbol
          \rEx. 5.99
          \rPress enter to try again
          \r*******************''')
  else:
    return int(price_float * 100)


def clean_quantity(quantity_str):
  try:
    quantity_int = int(quantity_str)
  except ValueError:
    input('''
          \n*** QUANTITY ERROR ***
          \rThe quantity should be a whole number
          \rEx. 37
          \rPress enter to try again
          \r**********************''')
  else:
    return quantity_int


def clean_date(date_str):
  split_date = date_str.split('/')
  try:
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])
    date_obj = datetime.date(year, month, day)
  except ValueError:
    input('''
        \n*** DATE ERROR ***
        \rThe date format should include a valid month/date/year
        \rEx: 2/29/2022
        \rPress enter to try again
        \r******************''')
    return
  else:
    return date_obj


def add_csv():
  with open('inventory.csv') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
      product_in_db = session.query(Product).filter(Product.name==row[0]).one_or_none()
      if product_in_db == None:
        name = row[0]
        price = clean_price(row[1])
        quantity = clean_quantity(row[2])
        date_updated = clean_date(row[3])
        new_product = Product(name=name, price=price, quantity=quantity, date_updated=date_updated)
        session.add(new_product)
  session.commit()


if __name__ == '__main__':
  Base.metadata.create_all(engine)
  add_csv()

  for product in session.query(Product):
    print(product)