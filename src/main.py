from banking_system import BankingSystem
from account import Account
from typing import Optional

def create_account(bank: BankingSystem) -> Optional[Account]:
    """Creates a new account by prompting for name and initial balance.

    Uses the provided BankingSystem instance to create and store the account.

    Args:
        bank (BankingSystem): The banking system managing accounts.

    Returns:
        Optional[Account]: The created Account object if successful, else None.
    """
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
    
def login(bank: 'BankingSystem') -> Optional[Account]:
    """Login to an account by prompting for an account ID.

    Args:
        bank (BankingSystem): The banking system managing accounts.

    Returns:
        Optional[Account]: The Account object if login is successful, else None.

    Raises:
        ValueError: If the entered account ID is not a valid integer.
    """
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
    """Runs the main interactive loop of the Simple Banking System.

    Prompts users to create an account, log in, and perform operations like deposit,
    withdrawal, transfer, or quit. Persists changes to the banking system's CSV file.

    Args:
        bank (BankingSystem, optional): The banking system instance to use. If None,
            creates a new BankingSystem with default CSV path 'accounts.csv'.
            Defaults to None.

    """
    if bank is None:
        bank = BankingSystem(csv_path='accounts.csv')
    current_user = None # None if not logged in

    # The main interactive loop
    while True:
        if current_user is None:
            # if not logged in, prompt the user to log in
            print("Welcome to Simple Banking System.")
            exist_user = input("Do you have an account? Type 'yes' to login, or 'no' to create an account: ").strip().lower()
            # Create account for new user
            if exist_user == 'no':
                current_user = create_account(bank)
            # Log in for existing user
            elif exist_user == 'yes':
                current_user = login(bank)
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            # if logged in, prompt the user for actions: 'd' to deposit, 'w' to withdraw, 't' to transfer, or 'q' to quit
            user_input = input("Please enter 'd' to deposit, 'w' to withdraw, 't' to transfer, or 'q' to quit: ").strip().lower()
            # Deposit money
            if user_input == 'd':
                amount = input("Enter the amount to deposit: ")
                success, message = current_user.deposit(amount)
                if success:
                    bank.save_state()
                print(message)
            # Withdraw money
            elif user_input == 'w':
                amount = input("Enter the amount to withdraw: ")
                success, message = current_user.withdraw(amount)
                if success:
                    bank.save_state()
                print(message)
            # Transfer money
            elif user_input == 't':
                try:
                    recipient_id = int(input("Enter the recipient's account ID: "))
                except ValueError:
                    print("Invalid account ID. Please try again.")
                    continue
                
                # Handle transfer money to the same account
                if current_user.id == recipient_id:
                    print("Cannot transfer to the same account!")
                    continue

                recipient = bank.get_account(recipient_id)
                # Handle non-existent recipient
                if not recipient:
                    print(f"Recipient with ID {recipient_id} does not exist.")
                    continue

                amount = input("Enter the amount to transfer: ")
                success, message = current_user.transfer(amount, recipient_id, bank)
                if success:
                    bank.save_state()
                print(message)
            # Logout
            elif user_input == 'q':
                print("Thank you for using the Simple Banking System. Goodbye!")
                break
            # Handle invalid user's input command
            else:
                print("Invalid input. Please enter 'd', 'w', 't', or 'q'.")

if __name__ == "__main__":
    main()
