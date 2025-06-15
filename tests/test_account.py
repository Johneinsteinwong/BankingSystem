import pytest
from account import Account
from banking_system import BankingSystem
from decimal import Decimal

# Initialize account with name="Alice" and balance=100
@pytest.fixture
def account():
    return Account(id=1, name="Alice", balance=Decimal('100'))

@pytest.fixture
def bank_system(tmp_path):
    csv_path = tmp_path / "accounts.csv"
    bank = BankingSystem(csv_path=str(csv_path))
    bank.accounts = {}  # Reset accounts
    return bank

# Deposit valid positive amount
def test_deposit_valid(account):
    success, message = account.deposit("50")
    assert success # successful flag
    assert account.balance == Decimal('150') # 50 + 100 == 150
    assert "Deposited 50" in message # Successful message

# Test for rounding error
def test_deposit_valid(account):
    # Using floating point number to calculate 100 + 0.1 + 0.1 would result in 100.19999999999999
    success, message = account.deposit("0.1")
    success, message = account.deposit("0.1")

    assert account.balance == Decimal('100.2') # Using Decimal would result in 100.2 correctly

# Deposit invalid negative amount
def test_deposit_negative(account):
    success, message = account.deposit("-50")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Deposit amount must be positive!" # Not successful message

# Deposit invalid 0 amount
def test_deposit_zero(account):
    success, message = account.deposit("0")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Deposit amount must be positive!" # Not successful message

# Deposit invalid non number string
def test_deposit_non_numeric(account):
    success, message = account.deposit("abc")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Invalid input, please input numbers only!" # Not successful message

# Deposit invalid NaN amount
def test_deposit_nan(account):
    success, message = account.deposit("NaN")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Invalid input, please input numbers only!" # Not successful message

# Deposit invalid Infinity amount
def test_deposit_infinity(account):
    success, message = account.deposit("Infinity")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Invalid input, please input numbers only!" # Not successful message

# Withdraw valid positive amount
def test_withdraw_valid(account):
    success, message = account.withdraw("50")
    assert success #successful flag
    assert account.balance == Decimal('50') # 100 - 50 == 50
    assert "Withdrew 50" in message # Successful message

# Withdraw overdraft
def test_withdraw_overdraft(account):
    success, message = account.withdraw("150")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Insufficient balance!" # Insufficient balance message

# Withdraw invalid negative amount
def test_withdraw_negative(account):
    success, message = account.withdraw("-50")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Withdrawal amount must be positive!" # Not successful message

# Withdraw invalid non number string
def test_withdraw_non_numeric(account):
    success, message = account.withdraw("abc")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Invalid input, please input numbers only!" # Not successful message

# Withdraw invalid NaN amount
def test_withdraw_nan(account):
    success, message = account.withdraw("NaN")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Invalid input, please input numbers only!" # Not successful message

# Withdraw invalid Infinity amount
def test_withdraw_infinity(account):
    success, message = account.withdraw("Infinity")
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # balance unchanged
    assert message == "Invalid input, please input numbers only!" # Not successful message

# Transfer valid positive amount
def test_transfer_valid(bank_system, account):
    recipient = Account(id=2, name="Bob", balance=Decimal('50')) # Create recipient account with balance 50
    bank_system.accounts = {
        1: account, 
        2: recipient
    }
    success, message = account.transfer("30", 2, bank_system) # Transfer 30 to recipient account
    assert success # Successful flag
    assert account.balance == Decimal('70') # 100 - 30 == 70
    assert recipient.balance == Decimal('80') # 50 + 30 == 80
    assert "Transferred 30" in message # Successful message

# Transfer overdraft
def test_transfer_insufficient_funds(bank_system, account):
    recipient = Account(id=2, name="Bob", balance=Decimal('50')) # Create recipient account with balance 50
    bank_system.accounts = {
        1: account, 
        2: recipient
    }
    success, message = account.transfer("150", 2, bank_system) # Balance = 100, but transfer 150
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # sender balance unchanged
    assert recipient.balance == Decimal('50') # recipient balance unchanged
    assert message == "Insufficient balance!" # Insufficient balance message

# Transfer invalid negative amount
def test_transfer_negative(bank_system, account):
    recipient = Account(id=2, name="Bob", balance=Decimal('50'))
    bank_system.accounts = {
        1: account, 
        2: recipient
    }
    success, message = account.transfer("-30", 2, bank_system) # Transfer -30 to recipient account
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # sender balance unchanged
    assert recipient.balance == Decimal('50') # recipient balance unchanged
    assert message == "Transfer amount must be positive!" # Not successful message

# Transfer invalid non number string
def test_transfer_non_numeric(bank_system, account):
    recipient = Account(id=2, name="Bob", balance=Decimal('50'))
    bank_system.accounts = {
        1: account, 
        2: recipient
    }
    success, message = account.transfer("abc", 2, bank_system) # Transfer 'abc' to recipient account
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # sender balance unchanged
    assert recipient.balance == Decimal('50') # recipient balance unchanged
    assert message == "Invalid input, please input numbers only!" # Not successful message

# Transfer invalid NaN amount
def test_transfer_nan(bank_system, account):
    recipient = Account(id=2, name="Bob", balance=Decimal('50'))
    bank_system.accounts = {
        1: account, 
        2: recipient
    }
    success, message = account.transfer("NaN", 2, bank_system) # Transfer 'NaN' to recipient account
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # sender balance unchanged
    assert recipient.balance == Decimal('50') # recipient balance unchanged
    assert message == "Invalid input, please input numbers only!" # Not successful message

# Transfer invalid 'Infinity' amount
def test_transfer_infinity(bank_system, account):
    recipient = Account(id=2, name="Bob", balance=Decimal('50'))
    bank_system.accounts = {
        1: account, 
        2: recipient
    }
    success, message = account.transfer("Infinity", 2, bank_system) # Transfer 'Infinity' to recipient account
    assert not success # unsuccessful flag
    assert account.balance == Decimal('100') # sender balance unchanged
    assert recipient.balance == Decimal('50') # recipient balance unchanged
    assert message == "Invalid input, please input numbers only!" # Not successful message