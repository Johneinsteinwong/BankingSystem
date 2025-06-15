import csv
from decimal import Decimal
from typing import Dict, Tuple, Optional
from account import Account
from utils import convert_decimal

class BankingSystem:
    def __init__(self, csv_path: str = 'accounts.csv'):
        self.csv_path = csv_path
        self.accounts: Dict[int, Account] = self.load_state()

    def load_state(self) -> Dict[int, Account]:
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
        try:
            initial_balance = convert_decimal(initial_balance)
        except (ValueError, TypeError) as err:
            return None, str(err)
        
        if initial_balance < 0:
            return None, "Initial balance cannot be negative!"
        
        account_id = max([acc for acc in self.accounts], default=0) + 1 # increment acc id
        account = Account(
                id = account_id,
                name = name,
                balance = initial_balance
            )
        self.accounts.update({
            account_id : account
        })
        self.save_state()
        return account, f"Account created for {account.name} with ID {account.id} and initial balance {initial_balance}."
    
    def get_account(self, account_id: int) -> Optional[Account]:
        account = self.accounts.get(account_id, None)
        return account
    
