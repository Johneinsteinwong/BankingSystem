import pytest
import csv
from banking_system import BankingSystem
from account import Account
from decimal import Decimal

# Initiate BankingSystem
@pytest.fixture
def banking_system(tmp_path):
    csv_path = tmp_path / "accounts.csv"
    bank = BankingSystem()
    bank.accounts = {} 
    return bank

# Test create_account() function with valid balance
def test_create_account_valid(banking_system):
    account, message = banking_system.create_account("Alice", "100")
    # Verify information of the created account
    assert account is not None
    assert account.id == 1
    assert account.name == "Alice"
    assert account.balance == Decimal('100')
    assert "Account created for Alice" in message
    assert len(banking_system.accounts) == 1

# Test create_account() function with invalid negative balance
def test_create_account_negative_balance(banking_system):
    account, message = banking_system.create_account("Alice", "-100")
    # No account should be included
    assert account is None
    assert "Initial balance cannot be negative" in message
    assert len(banking_system.accounts) == 0

# Test create_account() function with invalid non numberic balance
def test_create_account_non_numeric_balance(banking_system):
    account, message = banking_system.create_account("Alice", "abc")
    # No account should be included
    assert account is None
    assert "Invalid input, please input numbers only" in message
    assert len(banking_system.accounts) == 0

# Test create_account() function with invalid 'NaN' balance
def test_create_account_nan(banking_system):
    account, message = banking_system.create_account("Alice", "NaN")
    # No account should be included
    assert account is None
    assert "Invalid input, please input numbers only!" in message
    assert len(banking_system.accounts) == 0

# Test create_account() function with invalid 'Infinity' balance
def test_create_account_infinity(banking_system):
    account, message = banking_system.create_account("Alice", "Infinity")
    # No account should be included
    assert account is None
    assert "Invalid input, please input numbers only!" in message
    assert len(banking_system.accounts) == 0

# Test get_account() function with valid account_id
def test_get_account_valid(banking_system):
    account, _ = banking_system.create_account("Alice", "100")
    retrieved = banking_system.get_account(1)
    # Retrived account should be equal to created account
    assert retrieved == account

# Test get_account() function with invalid non-existent account_id
def test_get_account_invalid(banking_system):
    retrieved = banking_system.get_account(999)
    # No account should be retrieved
    assert retrieved is None

# Test get_account() function with invalid non-number account_id
def test_get_account_non_numeric(banking_system):
    retrieved = banking_system.get_account("abc")
    # No account should be retrieved
    assert retrieved is None

# Test save_state() function with one account in BankingSystem
def test_load_save_state(tmp_path):
    csv_path = tmp_path / "accounts.csv"
    # Create BankingSystem with account "Alice" and initial_balance "100"
    bank = BankingSystem()
    bank.accounts = {}
    bank.create_account(name="Alice", initial_balance='100')
    bank.save_state()
    
    # Successfully load the saved BankingSystem with account "Alice" and initial_balance "100"
    new_bank = BankingSystem()
    new_bank.load_state()
    print(new_bank.accounts)
    assert len(new_bank.accounts) == 1 # We only saved one account
    assert new_bank.accounts[1].id == 1
    assert new_bank.accounts[1].name == "Alice"
    assert new_bank.accounts[1].balance == Decimal('100')

# Test save_state() function with no accounts in BankingSystem
def test_load_empty_file(tmp_path):
    csv_path = tmp_path / "accounts.csv"
    # Create BankingSystem without any accounts
    bank = BankingSystem()
    bank.accounts = {}
    bank.save_state()

    # The loaded BankingSystem should contain no accounts
    new_bank = BankingSystem()
    new_bank.accounts = {}
    new_bank.load_state()
    assert len(new_bank.accounts) == 0
