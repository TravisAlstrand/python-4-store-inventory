from models import (Base, session, Product, engine)
import datetime
import csv
import time

def menu():
  while True:
    print('''
          \n*** STORE INVENTORY ***
          \r*** MAIN MENU ***
          \rView Single Product Details - (v)
          \rAdd a new product - (a)
          \rBackup Entire Database - (b)
          \rQuit (q)''')
    choice = input('\nWhat would you like to do? ').lower()
    if choice in ['v', 'a', 'b', 'q']:
      return choice
    else:
      input('''
            \nPlease choose one of the options above.
            \rEither v, a, b or q.
            \rPress enter to try again.''')


def clean_id(id_str, id_options):
  try:
    product_id_int = int(id_str)
  except ValueError:
    input('''
          \n*** ID ERROR ***
          \rThe ID should be a number from the list provided.
          \rPress enter to try again
          \r****************''')
    return
  else:
    if product_id_int in id_options:
      return product_id_int
    else:
      input(f'''
            \n*** ID ERROR ***
            \rPlease only enter an ID from the options provided.
            \rPress enter to try again
            \r****************''')
      return

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


def create_product(name, price, quantity, date):
  new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date)
  session.add(new_product)
  session.commit()

def edit_product(og, name, price, quantity, date):
  og.product_name = name
  og.product_price = price
  og.product_quantity = quantity
  og.date_updated = date


def build_product(row):
    name = row[0]
    price = clean_price(row[1])
    quantity = clean_quantity(row[2])
    date = clean_date(row[3])
    create_product(name, price, quantity, date)


def backup_to_new_csv():
  with open('backup.csv', 'w') as csvfile:
    fieldnames = ['product_name', 'product_price', 'product_quantity', 'date_updated']
    inventory_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    inventory_writer.writeheader()
    for product in session.query(Product):
      unclean_price = float(product.product_price / 100)
      unclean_date = product.date_updated.strftime('%m/%d/%Y')
      if unclean_date[3] == '0':
        unclean_date = unclean_date[:3] + unclean_date[4:]
      if unclean_date[0] == '0':
        unclean_date = unclean_date[1:]
      inventory_writer.writerow({
        'product_name': product.product_name,
        'product_price': '${0:.2f}'.format(unclean_price),
        'product_quantity': product.product_quantity,
        'date_updated': unclean_date
      })
  print('\nBackup successful!')
  print('\nReturning to main menu...')
  time.sleep(2.5)


def add_csv_to_db():
  with open('inventory.csv') as csvfile:
    data = csv.reader(csvfile)
    # SKIP HEADER LINE
    next(data)
    for row in data:
      product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
      if product_in_db == None:
        build_product(row)
      else:
        if product_in_db.date_updated < clean_date(row[3]):
          session.delete(product_in_db)
          build_product(row)
        else:
          pass


def app():
  app_running = True
  while app_running:
    choice = menu()
    if choice == 'v':
      # VIEW PRODUCT
      id_options = []
      for product in session.query(Product):
        id_options.append(product.product_id)
      id_error = True
      while id_error:
        id_choice = input(f'''
                          \nPlease enter an ID from the options below to view.
                          \rID Options: {id_options}
                          \rProduct ID: ''')
        id_choice = clean_id(id_choice, id_options)
        if type(id_choice) == int:
          id_error = False
      searched_product = session.query(Product).filter(Product.product_id==id_choice).first()
      print(f'''
            \nProduct Name: {searched_product.product_name}
            \rProduct Price: ${searched_product.product_price / 100}
            \rProduct Quantity: {searched_product.product_quantity}
            \rDate Updated: {searched_product.date_updated}''')
      print('\nReturning to main menu ... ')
      time.sleep(2.5)
    elif choice == 'a':
      # ADD PRODUCT
      name = input('Product Name: ')
      price_error = True
      while price_error:
        price = input('Product Price (Ex: 29.99): ')
        price = clean_price(price)
        if type(price) == int:
          price_error = False
      quantity_error = True
      while quantity_error:
        quantity = input('Product Quantity: ')
        quantity = clean_quantity(quantity)
        if type(quantity) == int:
          quantity_error = False
      date = datetime.date.today()
      # CHECK IF PRODUCT EXISTS IN DB
      product_in_db = session.query(Product).filter(Product.product_name==name).one_or_none()
      # IF NOT CREATE PRODUCT
      if product_in_db == None:
        create_product(name, price, quantity, date)
        print('Product added successfully!')
      # IF EXISTS UPDATE TO NEWEST
      else:
        if date >= product_in_db.date_updated:
          edit_product(product_in_db, name, price, quantity, date)
          print('Product updated successfully!')
        else:
          print('Most recent product reserved.')
      print('\nPrinting inventory ... ')
      time.sleep(2.5)
      for product in session.query(Product):
        print(product)
      print('\nReturning to main menu ...')
      time.sleep(2.5)
    elif choice == 'b':
      # BACKUP INVENTORY
      backup_to_new_csv()
    elif choice == 'q':
      # QUIT
      print('Thanks for stopping by!')
      quit()
      

if __name__ == '__main__':
  Base.metadata.create_all(engine)
  add_csv_to_db()
  app()
