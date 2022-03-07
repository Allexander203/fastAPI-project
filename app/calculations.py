def add(num1: int, num2: int):
    return num1 + num2

def subtract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1 * num2

def divide(num1: int, num2: int):
    return num1 / num2

class insufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, strarting_balance=0):
        self.balance = strarting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise insufficientFunds("Insufficient money in account")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
