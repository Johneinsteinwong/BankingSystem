from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Tuple
from utils import convert_decimal


class Account(BaseModel):
    id: int
    name: str
    balance: Decimal = Field(ge=0) # Use Decimal for arithmetic to avoid rounding errors

    def deposit(self, amount: str) -> Tuple[bool, str]:
        try:
            amount = convert_decimal(amount)
        except (ValueError, TypeError) as err:
            return False, str(err)
        
        if amount <= 0:
            return False, "Deposit amount must be positive!"
        
        self.balance += amount

        return True, f"Deposited {amount} to account {self.id}. New balance: {self.balance}."
    
    def withdraw(self, amount: str) -> Tuple[bool, str]:
        try:
            amount = convert_decimal(amount)
        except (ValueError, TypeError) as err:
            return False, str(err)
        
        if amount <= 0:
            return False, "Withdrawal amount must be positive!"
        
        if amount > self.balance:
            return False, "Insufficient balance!"
        
        self.balance -= amount

        return True, f"Withdrew {amount} from account {self.id}. New balance: {self.balance}"
    
    def transfer(self, amount: str, recipient_id: int, bank: 'BankingSystem') -> Tuple[bool, str]:
        try:
            amount = convert_decimal(amount)
        except (ValueError, TypeError) as err:
            return False, str(err)
        
        if amount <= 0:
            return False, "Transfer amount must be positive!"
        
        if amount > self.balance:
            return False, "Insufficient balance!"
        
        recipient = bank.get_account(recipient_id)
        
        self.balance -= amount
        recipient.balance += amount

        return True, f"Transferred {amount} to account {recipient_id}. New balance: {self.balance}"

