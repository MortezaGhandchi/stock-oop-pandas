from decimal import Decimal


class Account:
    """
    Account class maintain information and balance about each account
    ******Arguments******
    firstname:string
    lastname:string
    national id number:string with 10 numbers
    birthdate:string in the form of ##/##/####
    balance:integer greater than or equal to zero
    """
    accountNumber = 0
    accountsList = []

    def __init__(self, firstname, lastname, national_id_number, birthdate, balance):
        self.firstname = firstname
        self.lastname = lastname
        self.national_id_number = national_id_number
        self.birthdate = birthdate
        self.balance = balance
        Account.accountNumber += 1
        self.account_number = Account.accountNumber
        self.stocks = {}  # {stock symbol: [shares, value]}
        Account.accountsList.append(self)

    def __str__(self):
        return f"{self.account_number}) {self.firstname:<9} {self.lastname:<9} Id:[{self.national_id_number}] " \
               f"  Birthdate:[{self.birthdate}]   Balance = {self.balance:,}"

    def buy_shares(self, stock, shares):
        """
        function to buy some shares from specific stock
        :param stock: Stock object
        :param shares: positive integer (representing Number of shares purchased)
        :return: string (Notify transaction completed successfully)
        """
        value = shares * stock.open_val
        if type(shares) != int:
            raise TypeError("Shares must be integer")
        elif shares > stock.shares_remain:
            raise ValueError(f"Shares value must be lower than remaining shares for stock ({stock.shares_remain})")
        elif shares < 1:
            raise ValueError("Shares must be positive integer")
        elif value > self.balance:
            raise ValueError("Not enough money for account to buy these shares")
        elif stock.symbol not in self.stocks:
            self.stocks[stock.symbol] = [shares, value]
        else:
            self.stocks[stock.symbol][0] += shares
            self.stocks[stock.symbol][1] += value
        self.balance = int(self.balance - value)
        stock.shares_remain -= shares
        return f"{self.firstname} {self.lastname} bought {shares} {stock.symbol} shares successfully"

    def sell_shares(self, stock, shares):
        """
        function to sell some shares from specific stock
        :param stock: Stock object
        :param shares: positive integer (representing Number of shares sold)
        :return: string (Notify transaction completed successfully)
        """
        sellValue = shares * stock.open_val
        cShares, cValue = self.stocks[stock.symbol]
        if stock.symbol not in self.stocks:
            raise ValueError("Account Doesn't have this stock")
        elif type(shares) != int:
            raise TypeError("Shares must be integer")
        elif shares < 1:
            raise ValueError("Shares must be positive integer")
        elif shares > cShares:
            raise ValueError(f"Not enough shares for account to sell ({cShares})")
        else:
            self.stocks[stock.symbol][0] -= shares
            self.stocks[stock.symbol][1] -= sellValue
        self.balance = int(self.balance + sellValue)
        stock.shares_remain += shares
        return f"{self.firstname} {self.lastname} sold {shares} {stock.symbol} shares successfully"

    def get_shares(self):
        """
        function to print shares that belongs to account
        :return: string (Total shares and values)
        """
        if not self.stocks:
            return f"{self.firstname} {self.lastname} doesn't have any share"
        counter = 0
        total_shares = 0
        total_value = 0
        print(f"{self.firstname} {self.lastname} shares:")
        for k, v in self.stocks.items():
            total_shares += v[0]
            total_value += v[1]
            counter += 1
            print(f"[{counter}] {k:<6} Shares:{v[0]:<7,}   Value = {v[1]:,.0f}")
        return f"Total shares:{total_shares:<7,}   Total value = {total_value:,.0f}"

    @property
    def firstname(self):
        return self.__firstname

    @firstname.setter
    def firstname(self, value):
        if type(value) != str:
            raise TypeError("Firstname must be string")
        elif not value.replace(" ", "").isalpha():
            raise ValueError("Firstname must be consists of only alphabetic characters")
        else:
            self.__firstname = value

    @property
    def lastname(self):
        return self.__lastname

    @lastname.setter
    def lastname(self, value):
        if type(value) != str:
            raise TypeError("Firstname must be string")
        elif not value.replace(" ", "").isalpha():
            raise ValueError("Lastname must be consists of only alphabetic characters")
        else:
            self.__lastname = value

    @property
    def national_id_number(self):
        return self.__national_id_number

    @national_id_number.setter
    def national_id_number(self, value):
        if type(value) != str:
            # I choose string because it is not possible to place 0 left side of the id numbers if they were integer
            raise TypeError("National id number must be string")
        elif len(value) != 10 or not value.isdigit():
            raise ValueError("National id number must be consists of 10 numbers")
        else:
            self.__national_id_number = value

    @property
    def birthdate(self):
        return self.__birthdate

    @birthdate.setter
    def birthdate(self, value):
        if type(value) != str:
            raise TypeError("Birthdate must be string")
        elif len(value) != 10 or not value.replace("/", "").isdigit() or not value[2] == value[5] == "/":
            raise ValueError("Birthdate must be in the form of ##/##/####, where each # is a digit")
        else:
            self.__birthdate = value

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if type(value) != int:
            raise TypeError("Balance must be integer")
        elif not value >= 0:
            raise ValueError("Balance must be greater than or equal to zero")
        else:
            self.__balance = Decimal(value)


def print_account_list():
    """
    Function to print all existing accounts
    """
    for account in Account.accountsList:
        print(account)


class Stock:
    """
    Stock class maintain current information such as open, volume and number of shares about each company
    ******Arguments******
    symbol:string (abbreviation for company name)
    open val:float greater than zero (price for each stock that belongs to the company)
    volume:integer greater than zero (price for all of stocks that belongs to the company)
    date:string
    """
    companyNumber = 0
    stocksList = []

    def __init__(self, symbol, open_val, volume, date):
        self.symbol = symbol
        self.open_val = open_val
        self.volume = volume
        self.date = date
        self.shares = self.volume // self.open_val
        self.shares_remain = self.shares
        Stock.companyNumber += 1
        self.company_number = Stock.companyNumber
        Stock.stocksList.append(self)

    def __str__(self):
        return f"{self.company_number}) {self.symbol:<6} Open = {self.open_val:<11,.2f} Volume = {self.volume:<13,} " \
               f"Total shares:{self.shares:<7,}    Sold shares:{self.shares - self.shares_remain:<7,}  date:{self.date}"

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, value):
        if type(value) != str:
            raise TypeError("symbol must be string")
        self.__symbol = value

    @property
    def open_val(self):
        return self.__open_val

    @open_val.setter
    def open_val(self, value):
        if type(value) != float:
            raise TypeError("Open value must be float")
        elif not value > 0:
            raise ValueError("Open value must be greater than zero")
        else:
            self.__open_val = Decimal(value)

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, value):
        if type(value) != int:
            raise TypeError("Volume must be integer")
        elif not value > 0:
            raise ValueError("Volume must be greater than zero")
        else:
            self.__volume = Decimal(value)

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        if type(value) != str:
            raise TypeError("Date must be string")
        self.__date = value


def print_stock_list():
    """
    Function to print all existing stocks
    """
    for stock in Stock.stocksList:
        print(stock)


account1 = Account("Ali", "Ronaldo", "0045375980", "01/10/2000", 15000)
account2 = Account("majid", "messy", "0025328985", "10/16/2002", 10000)
print_account_list()
amazon = Stock("AMZN", 2181.3798828125, 4676700, "05/13/2022")
facebook = Stock("FB", 192.580001831054, 24523500, "05/13/2022")
tesla = Stock("TSLA", 773.47998046875, 30651800, "05/13/2022")
google = Stock("GOOGLE", 2290.65991210937, 1747900, "05/13/2022")
apple = Stock("AAPL", 144.58999633789, 113787000, "05/13/2022")
print_stock_list()
print(account1)
account1.buy_shares(apple, 10)
account1.buy_shares(apple, 5)
account1.buy_shares(facebook, 11)
account1.sell_shares(facebook, 2)
account1.get_shares()
print(account1)
print(apple)
