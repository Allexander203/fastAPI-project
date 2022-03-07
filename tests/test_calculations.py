import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, insufficientFunds

@pytest.fixture
def zero_bank_acc():
    return BankAccount()

@pytest.fixture
def bank_acc():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])

# the naming matters, so the name should start with the word test_* *is the name of the module which is testing
def test_add(num1, num2, expected):
    print("creating empty bank account")
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(4, 3) == 12


def test_divide():
    assert divide(20, 5) == 4


def test_bank_set_initial_amount(bank_acc):
    assert bank_acc.balance == 50


def test_bank_default_amount(zero_bank_acc):
    print("testing my bank account")
    assert zero_bank_acc.balance == 0


def test_withdraw(bank_acc):
    bank_acc.withdraw(20)
    assert bank_acc.balance == 30


def test_deposit(bank_acc):
    bank_acc.deposit(20)
    assert bank_acc.balance == 70


def test_collect_interest(bank_acc):
    bank_acc.collect_interest()
    assert round(bank_acc.balance, 6) == 55


@pytest.mark.parametrize("deposit, withdraw, expected", [
    (200,100,100),
    (50,10,40),
    (1200,200,1000),
])

def test_bank_transaction(zero_bank_acc, deposit, withdraw, expected):
    zero_bank_acc.deposit(deposit)
    zero_bank_acc.withdraw(withdraw)
    assert zero_bank_acc.balance == expected

def test_insufficient_funds(bank_acc):
    with pytest.raises(insufficientFunds):
        bank_acc.withdraw(200)
