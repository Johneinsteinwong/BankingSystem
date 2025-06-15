import csv
from decimal import Decimal
from typing import Dict, Tuple, Optional
from account import Account
from utils import convert_decimal

class BankingSystem:
    """Manages bank accounts, storing them in a dictionary and persisting to a CSV file.

    Attributes:
        csv_path (str): Path to the CSV file for storing account data.
        accounts (Dict[int, Account]): Dictionary mapping account IDs to Account objects.
    """
    def __init__(self, csv_path: str = 'accounts.csv'):
        """Initializes a BankingSystem instance, loading accounts from a CSV file.
        Args:
            csv_path (str, optional): Path to the CSV file. Defaults to 'accounts.csv'.
        """
        self.csv_path = csv_path
        self.accounts: Dict[int, Account] = self.load_state()

    def load_state(self) -> Dict[int, Account]:
        """Loads account data from the CSV file into a dictionary and returns it.

        If the CSV file does not exist, creates an empty file with headers.

        Returns:
            Dict[int, Account]: Dictionary of account IDs to Account objects.

        Raises:
            FileNotFoundError: If the CSV file cannot be found, FileNotFoundError is raised and create it.
        """
        accounts = {}
        try:
            # read accounts if the csv file exists
            with open(self.csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    account_id = int(row['id'])
                    accounts.update({
                        account_id:
                        Account(
                            id = account_id, 
                            name = row['name'], 
                            balance = Decimal(row['balance'])
                        )
                    })
        except FileNotFoundError:
            # create the csv file if not exists
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['id','name','balance'])
                writer.writeheader()
        return accounts
    
    def save_state(self) -> None:
        """Saves the current accounts to the CSV file.

        Overwrites the existing file with current account data.

        """
        with open(self.csv_path,'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id','name','balance'])
            writer.writeheader()
            for account in self.accounts.values():
                writer.writerow({
                    'id': account.id,
                    'name': account.name,
                    'balance': account.balance
                })

    def create_account(self, name: str, initial_balance: str) -> Tuple[Optional[Account],str]:
        """Creates a new account with the given name and initial balance.

        Args:
            name (str): The account holder's name.
            initial_balance (str): The initial balance as a string representation of a number.

        Returns:
            Tuple[Optional[Account], str]: A tuple containing the created Account object (or None if
                creation failed) and a message describing the outcome.

        Raises:
            ValueError: If initial_balance is not a valid decimal number.
            TypeError: If initial_balance cannot be converted to a decimal.
        """
        try:
            initial_balance = convert_decimal(initial_balance)
        except (ValueError, TypeError) as err:
            return None, str(err)
        
        # Handle negative initial_balance
        if initial_balance < 0:
            return None, "Initial balance cannot be negative!"
        
        account_id = max([acc for acc in self.accounts], default=0) + 1 # increment acc id
        account = Account(
                id = account_id,
                name = name,
                balance = initial_balance
            )
        # Append created account to account dictionary
        self.accounts.update({
            account_id : account
        })
        self.save_state()
        return account, f"Account created for {account.name} with ID {account.id} and initial balance {initial_balance}."
    
    def get_account(self, account_id: int) -> Optional[Account]:
        """Retrieves an account by its ID.

        Args:
            account_id (int): The ID of the account to retrieve.

        Returns:
            Optional[Account]: The Account object if found, else None.
        """
        account = self.accounts.get(account_id, None)
        return account
    
