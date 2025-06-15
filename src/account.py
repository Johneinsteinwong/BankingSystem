from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Tuple
from utils import convert_decimal


class Account(BaseModel):
    """Represents a bank account with an ID, name, and balance.

    Uses Pydantic for data validation and Decimal for precise arithmetic.

    Attributes:
        id (int): Unique identifier for the account.
        name (str): Account holder's name. Can be non-unique, since id is the unique identifier instead
        balance (Decimal): Current balance, must be non-negative.
    """
    id: int
    name: str
    balance: Decimal = Field(ge=0) # Use Decimal for arithmetic to avoid rounding errors, should be >= 0

    def deposit(self, amount: str) -> Tuple[bool, str]:
        """Deposits a specified amount into the account.

        Args:
            amount (str): The amount to deposit as a string representation of a number.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating success flag and a message
                describing the outcome.

        Raises:
            ValueError: If amount is not a valid decimal number.
            TypeError: If amount cannot be converted to a decimal.
        """
        try:
            amount = convert_decimal(amount)
        except (ValueError, TypeError) as err:
            return False, str(err)
        
        # Handle negative amount
        if amount <= 0:
            return False, "Deposit amount must be positive!"
        
        self.balance += amount

        return True, f"Deposited {amount} to account {self.id}. New balance: {self.balance}."
    
    def withdraw(self, amount: str) -> Tuple[bool, str]:
        """Withdraws a specified amount from the account.

        Args:
            amount (str): The amount to withdraw as a string representation of a number.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating success flag and a message
                describing the outcome.

        Raises:
            ValueError: If amount is not a valid decimal number.
            TypeError: If amount cannot be converted to a decimal.
        """
        try:
            amount = convert_decimal(amount)
        except (ValueError, TypeError) as err:
            return False, str(err)
        
        # Handle negative amount
        if amount <= 0:
            return False, "Withdrawal amount must be positive!"
        
        # Handle insufficient balance
        if amount > self.balance:
            return False, "Insufficient balance!"
        
        self.balance -= amount

        return True, f"Withdrew {amount} from account {self.id}. New balance: {self.balance}"
    
    def transfer(self, amount: str, recipient_id: int, bank: 'BankingSystem') -> Tuple[bool, str]:
        """Transfers a specified amount to a recipient account. 
        Non-existent recipient account is handled in main.py.

        Args:
            amount (str): The amount to transfer as a string representation of a number.
            recipient_id (int): The ID of the recipient's account.
            bank (BankingSystem): The banking system managing accounts.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating success flag and a message
                describing the outcome.

        Raises:
            ValueError: If amount is not a valid decimal number.
            TypeError: If amount cannot be converted to a decimal.  
        """
        try:
            amount = convert_decimal(amount)
        except (ValueError, TypeError) as err:
            return False, str(err)
        
        # Handle negative amount
        if amount <= 0:
            return False, "Transfer amount must be positive!"
        
        # Handle insufficient balance
        if amount > self.balance:
            return False, "Insufficient balance!"
        
        recipient = bank.get_account(recipient_id)
        
        self.balance -= amount
        recipient.balance += amount

        return True, f"Transferred {amount} to account {recipient_id}. New balance: {self.balance}"

