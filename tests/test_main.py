import pytest
from main import main, create_account, login
from banking_system import BankingSystem
from decimal import Decimal
from unittest.mock import patch

# Initiate BankingSystem
@pytest.fixture
def bank_system(tmp_path):
    csv_path = tmp_path / "accounts.csv"
    bank = BankingSystem(csv_path=str(csv_path))
    bank.accounts = {}
    return bank

# Test create_account() function with valid balance
def test_create_account_valid(capsys, bank_system):
    with patch('builtins.input', side_effect=["Alice", "100"]):
        account = create_account(bank_system)
    captured = capsys.readouterr()
    # Verify information of the created account
    assert account is not None
    assert account.id == 1
    assert account.name == "Alice"
    assert account.balance == Decimal('100')
    assert "Account created for Alice" in captured.out

# Test the login() function with valid account_id
def test_login_valid(capsys, bank_system):
    bank_system.create_account("Alice", "100")
    with patch('builtins.input', side_effect=["1"]): # Login with accound_id = 1
        account = login(bank_system)
    captured = capsys.readouterr()
    # Verify account information
    assert account is not None
    assert account.id == 1
    assert "Welcome back, Alice" in captured.out

# Test the login() function with invalid non-existent account_id
def test_login_invalid_id(capsys, bank_system):
    with patch('builtins.input', side_effect=["999"]): # Login with non-existent accound_id = 999
        account = login(bank_system)
    captured = capsys.readouterr()
    # Should be unable to login
    assert account is None
    assert "Invalid account ID" in captured.out

# Transfer to invalid recipient_id
def test_transfer_invalid_recipient_id(capsys, bank_system):
    bank_system.create_account("Alice", "100")
    with patch('builtins.input', side_effect=['yes','1','t', '999', 'q']): # Login and transfer to invalid recipient_id = 999
        main(bank=bank_system)
    captured = capsys.readouterr()
    # Should result in 'Recipient not exist' error
    assert "Recipient with ID 999 does not exist." in captured.out
    assert "Enter the amount to transfer:" not in captured.out

# Transfer to same account
def test_transfer_same_account(capsys, bank_system):
    bank_system.create_account("Alice", "100")
    with patch('builtins.input', side_effect=['yes','1','t', '1', 'q']): # Login with account_id = 1 and transfer to account_id = 1
        main(bank=bank_system)
    captured = capsys.readouterr()
    # Should result in 'transfer to the same account' error
    assert "Cannot transfer to the same account!" in captured.out
    assert "Enter the amount to transfer:" not in captured.out

# Valid fund transfer
def test_transfer_valid(capsys, bank_system):
    bank_system.create_account("Alice", "100")
    bank_system.create_account("Bob", "50")
    with patch('builtins.input', side_effect=['yes','1','t', '2', '30', 'q']): # Login with account_id = 1 and transfer to account_id = 2 with amount 30
        main(bank=bank_system)
    captured = capsys.readouterr()
    assert "Transferred 30 to account 2" in captured.out
    assert bank_system.get_account(1).balance == Decimal('70') # 100 - 30 == 70
    assert bank_system.get_account(2).balance == Decimal('80') # 50 + 30 == 80