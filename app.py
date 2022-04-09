# import models
from ssl import Options
from sqlalchemy import Integer
from models import (Base, session,
                    Book, engine)
import datetime
import csv
import time

class NotInListError(Exception):
    pass

class TitleError(Exception):
    pass

# add books to the database
# edit books
# delete books
# search books
# data cleaning

def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')

    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n****** DATE ERROR ******
            \rThe date format should include a valid Month Day, Year from the past.
            \rEx: October 14, 1980
            \rPress enter to try again.
            \r************************''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        return_int = int(float(price_str) * 100)
    except ValueError:
        input('''
            \n****** PRICE ERROR ******
            \rThe price should be a number without a current symbol.
            \rEx: 10.99
            \rPress enter to try again.
            \r*************************''')
        return
    else:
        return return_int


def clean_id(id_str, id_options):
    try:
        book_id = int(id_str)
        if book_id not in id_options:
            raise NotInListError
    except ValueError:
        input('''
            \n****** ID ERROR ******
            \rThe ID should be a number.
            \rEx: 10
            \rPress enter to try again.
            \r*************************''')
        return
    except NotInListError:
        input(f'''
            \n****** ID ERROR ******
            \rThe ID should be one that is in the following list.
            \rOptions: {id_options}
            \rPress enter to try again.
            \r*************************''')
        return
    else:
        return book_id

def title_in_db(title):
    try:
        title_check = session.query(Book).filter(Book.title==title).one_or_none()
        if title_check != None:
            raise TitleError
    except TitleError:
        input('''
            \n****** TITLE ERROR ******
            \rThat book already exists in the database.
            \rPress enter to try again.
            \r************************''')
        return True
    else:
        return False


def menu():
    while True:
        print('''
            \nPROGRAMMING BOOKS
            \r1) Add Book
            \r2) View all books
            \r3) Search for book by ID
            \r4) Book Analysis
            \r5) Exit''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
                \rPlease choose of the options above.
                \rA number from 1-5.
                \rPress enter to try again.''')


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
            else:
                print(f'"{book_in_db.title}" already exists in the database.')
        session.commit()
            

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            title_error = True
            while title_error:
                title = input('Title: ')
                title_error = title_in_db(title)
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date (Ex: October 25, 2017): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex: 9.99): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print(f'\n{new_book.title} successfully added to the database!')
            time.sleep(1.5)
            
            

        elif choice == '2':
            # view all books
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\nPress enter to return to the main menu...')
            
            
        elif choice == '3':
            # Search for book
            
            id_options = []
            
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nID Options: {id_options}
                    \rBook id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f'''
                \n{the_book.title} by {the_book.author}
                \rPublished: {the_book.published_date}
                \rPrice: ${the_book.price/100}''')
            input('\nPress Enter to return to the main menu...')
        elif choice == '4':
            # Book Analysis
            pass
        else:
            print('GOODBYE')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    
    