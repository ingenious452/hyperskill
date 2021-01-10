# Write your code here
import random
import sqlite3

#-------------------------------Card class--------------------------------
class Card:
    BIN = str(400000)    # Band ID default for all the cards


    def __init__(self, account_identifier):
        self.account_identifier = account_identifier
        self.card_number = None
        self.card_password = None
        self.create_card()  # Create card initial value


    # Validate the card number using Luhn algorithm
    def card_validator(self, card_15_digits):
        """return -> str() check sum after validating"""

        # Multiply by 2 if number are odd
        odd_index = [int(card_15_digits[i]) * 2 if (i + 1) % 2 != 0 else int(card_15_digits[i])
                     for i in range(len(card_15_digits))]
        # Subtract 9 if the number is > 9
        less_than_9 = [num - 9 if num > 9 else num for num in odd_index]
        for i in range(10):     # Find the check sum digit
            if (sum(less_than_9) + i) % 10 == 0:
                return str(i)


    def create_card(self):
        """Set the value for card attribute
            card_number = number validated using mod 10 algorithm
            card_password = random generated 4 digit number"""

        self.card_number = Card.BIN + self.account_identifier \
                           + self.card_validator(''.join([Card.BIN, self.account_identifier]))
        self.card_password = str(random.randint(1000, 9999))     # Create 4 digit psuedo random password
#------------------------------------------------------------------------------------------------------


#-----------------------------Account class------------------------------------------------------------
class Account:
    # Default menu option for accounts
    OPTIONS = ['1. Balance', '2. Add income', '3. Do transfer', '4. Close account', '5. Log out', '0. Exit']


    def __init__(self, database_object):
        self.account_identifier = str(random.randint(100000000, 999999999))
        self.balance = 0
        self.database_handler = database_object


    def is_valid_card(self, card_number):
        """check if reciever card number is valid according to Luhn algorithm"""
        odd_index = [int(card_number[i]) * 2 if (i + 1) % 2 != 0 else int(card_number[i])
                     for i in range(len(card_number[:15]))]     # multiply by 2 all odd indexed numbers
        # Subtract 9 if the number is > 9 in odd_index list
        less_than_9 = [num - 9 if num > 9 else num for num in odd_index]

        if (sum(less_than_9) + int(card_number[-1])) % 10 == 0:
            return True # if card is valid according to Luhn algorithm
        else:
            return False


    def make_transfer(self, sender_card_number):
        """Transfer money from one account to another"""
        print('Enter card number: ')
        receiver_card_number = input()

        if sender_card_number == receiver_card_number:
            print('You cant\'t transfer money to the same account\n')
        elif self.is_valid_card(receiver_card_number):
            if self.database_handler.get_card(receiver_card_number):
                print('Enter how much money you want to transfer: ')
                amount = int(input())
                if amount > self.database_handler.get_balance(sender_card_number):
                    print('Not enough money!\n')
                else:
                    self.database_handler.update_balance(amount, sender_card_number, True)
                    self.database_handler.update_balance(amount, receiver_card_number)
                    print('Success!\n')
            else:
                print('Such a card does not exist.\n')
        else:
            print('Probably you made a mistake in the card number. Please try again!\n')


    def display_menu(self):
        """Print the menu using for loop"""
        for option in Account.OPTIONS:
            print(option)


    def account_handler(self, card_number):
        """Handle the user choice with conditonal set flag
            has_exited = True
            if user exit without logging out"""

        has_exited = False    # flag
        while True:
            self.display_menu()
            try:
                user_choice = int(input())
            except ValueError:
                print('Invalid input')
                continue

            if user_choice == 1:
                self.balance = self.database_handler.get_balance(card_number)
                print(f'\nBalance: {self.balance}\n')
            elif user_choice == 2:
                print('\nEnter income: ')
                income = int(input())
                self.database_handler.update_balance(income, card_number)
                print('\nIncome was added!\n')

            elif user_choice == 3:
                print('\nTransfer')
                self.make_transfer(card_number)
            elif user_choice == 4:
                self.database_handler.delete_account(card_number)
                print('\nThe account has been closed!\n')
            elif user_choice == 5:
                print('\nYou have successfully logged out!\n')
                break
            else:
                has_exited = True
                break

        return has_exited   # return the exit flag
#--------------------------------------------------------------------------------------------------


#----------------------------------------DATABASE--------------------------------------------------
class DatabaseHandler:
    # create connection to database :- card.s3db
    CONNECTION = sqlite3.Connection('card.s3db')
    USER_COUNT = 0

    def __init__(self):
        """Create table when object is created"""
        self.create_table()


    def create_table(self):
        """Create a table card"""
        connection = DatabaseHandler.CONNECTION
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS card('
                       'id INTEGER'
                       'number TEXT,'
                       'pin TEXT,'
                       'balance INTEGER);')

        connection.commit()


    def delete_table(self):
        """Delete the table:-> card"""
        connection = DatabaseHandler.CONNECTION
        cursor = connection.cursor()
        cursor.execute('DROP TABLE card;')

        connection.commit()


    def delete_account(self, card_number):
        connection = DatabaseHandler.CONNECTION
        cursor = connection.cursor()
        cursor.execute('DELETE FROM card where number = ?', (card_number,))
        connection.commit()


    def get_balance(self, card_number):
        """Retrieve the user account balance"""
        connection = DatabaseHandler.CONNECTION
        cursor = connection.cursor()
        cursor.execute('SELECT balance FROM card WHERE number = ?', (card_number,))
        try:
            return cursor.fetchone()[0]
        except TypeError:
            return None


    def update_balance(self, amount, card_number, deduct=False):
        """Update the account balance"""
        connection = DatabaseHandler.CONNECTION
        cursor = connection.cursor()
        # retrieve the previously store balance instead of directly putting amount as new balance
        previous_balance = self.get_balance(card_number)
        # change balance based on flag
        if deduct:
            current_balance = previous_balance - amount
        else:
            current_balance = previous_balance + amount
        cursor.execute('UPDATE card SET balance = ? WHERE number = ? ', (current_balance, card_number))
        connection.commit()


    def get_card(self, card_number):
        """Check wether the card_number exist in database"""
        connection = DatabaseHandler.CONNECTION
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM card WHERE number = ?', (card_number,))
        try:
            values = cursor.fetchone()[0]
            return True
        except TypeError:
            return None



    def update_table(self, card_number, card_password, account_balance):
        """Update the database table card"""
        DatabaseHandler.USER_COUNT += 1
        connection = DatabaseHandler.CONNECTION
        cursor = connection.cursor()
        cursor.execute('INSERT INTO card(id, number, pin, balance) VALUES(?, ?, ?, ?)',
                       (DatabaseHandler.USER_COUNT, card_number, card_password, account_balance))
        connection.commit()


    def login(self, card_number, card_password):
        """Retrieve the given attribute from card table"""
        connection = DatabaseHandler.CONNECTION
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM card WHERE number = ? AND pin = ?',
                       (card_number, card_password))

        if cursor.fetchone():
            return True
        else:
            return False
#------------------------------------------------------------------------------------------------------


#------------------------------------Bank class---------------------------------------------------
class Bank:

    OPTIONS = ['1. Create an account', '2. Log into account', '0. Exit']
    database_handler = DatabaseHandler()     # create a DatabaseHandler object

    def issue_card(self, account_identifier):
        """Create card object"""

        black_card = Card(account_identifier)

        # Display the card detail
        print()
        print('Your card number:')
        print(black_card.card_number)
        print('Your card PIN:')
        print(black_card.card_password)
        print()

        return black_card   # Return -> card object


    def create_account(self):
        """Create account and card objects, update database"""
        account = Account(Bank.database_handler)     # create account object and pass the 9 digits random
                                                                    # account identifier
        card = self.issue_card(account.account_identifier)
        # Update table with new account card details
        Bank.database_handler.update_table(card.card_number, card.card_password, account.balance)
        return account


    def account_login(self, card_number, card_password, account_object):
        """Check if the creditentials are correct using database"""
        if Bank.database_handler.login(card_number, card_password):
            print('\nYou have successfully logged in!\n')
            return account_object.account_handler(card_number)
        else:
            print('\nWrong card number or PIN!\n')
            return False


    def display_main_screen(self):
        """Display option on screen"""
        for option in Bank.OPTIONS:
            print(option)


    def user_handler(self):
        """Provide interface to user with choices"""
        account_object = None
        while True:
            self.display_main_screen()
            user_choice = int(input())

            if user_choice == 1:
                account_object = self.create_account()
            elif user_choice == 2:
                print('\nEnter your card number: ')
                number = input()
                print('Enter your PIN: ')
                password = input()
                if self.account_login(number, password, account_object):
                    print('Bye!')
                    break
            else:
                print('Bye!')
                break
#-------------------------------------------------------------------------------------------------

moonlinaire = Bank()
moonlinaire.user_handler()
