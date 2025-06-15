import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from banking_system import BankingSystem
from account import Account

def create_account(bank: BankingSystem) -> None:
    name = input("Please enter your name to create an account: ")
    initial_balance = input("Please enter an initial balance: ")

    account, message = bank.create_account(name, initial_balance)

    if account:
        print(message)
        print("You can now login with your account ID.")
        return account
    else:
        print(message)
        return None
    
def login(bank: 'BankingSystem') -> Account:
    try:
        account_id = int(input("Please enter your account ID to login: "))
    except ValueError:
        print("Invalid account ID. Please try again.")
        return None
    
    account = bank.get_account(account_id)

    if account:
        print(f"Welcome back, {account.name}! Your current balance is {account.balance}.")
        return account
    else:
        print("Invalid account ID. Please try again.")
        return None
    
def main(bank: BankingSystem = None):
    if bank is None:
        bank = BankingSystem(csv_path='accounts.csv')
    current_user = None

    while True:
        if current_user is None:
            # if not logged in
            print("Welcome to Simple Banking System.")
            exist_user = input("Do you have an account? Type 'yes' to login, or 'no' to create an account: ").strip().lower()
            if exist_user == 'no':
                current_user = create_account(bank)

            elif exist_user == 'yes':
                current_user = login(bank)
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            # if logged in
            user_input = input("Please enter 'd' to deposit, 'w' to withdraw, 't' to transfer, or 'q' to quit: ").strip().lower()
            if user_input == 'd':
                amount = input("Enter the amount to deposit: ")
                success, message = current_user.deposit(amount)
                if success:
                    bank.save_state()
                print(message)
            elif user_input == 'w':
                amount = input("Enter the amount to withdraw: ")
                success, message = current_user.withdraw(amount)
                if success:
                    bank.save_state()
                print(message)
            elif user_input == 't':
                try:
                    recipient_id = int(input("Enter the recipient's account ID: "))
                except ValueError:
                    print("Invalid account ID. Please try again.")
                    continue

                if current_user.id == recipient_id:
                    print("Cannot transfer to the same account!")
                    continue

                recipient = bank.get_account(recipient_id)
                if not recipient:
                    print(f"Recipient with ID {recipient_id} does not exist.")
                    continue

                amount = input("Enter the amount to transfer: ")
                success, message = current_user.transfer(amount, recipient_id, bank)
                if success:
                    bank.save_state()
                print(message)
            elif user_input == 'q':
                print("Thank you for using the Simple Banking System. Goodbye!")
                break
            else:
                print("Invalid input. Please enter 'd', 'w', 't', or 'q'.")

if __name__ == "__main__":
    main()
